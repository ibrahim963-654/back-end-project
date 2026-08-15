
# ==========================================
# CORE UTILITIES
# ==========================================

from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Avg

from core.models import (
    Evaluation,
    Attendance,
    CompanySetting,
)

User = get_user_model()


# ==========================================
# GET CLIENT IP
# ==========================================

def get_client_ip(request):
    """
    استخراج IP الحقيقي للمستخدم.
    يدعم X-Forwarded-For في حالة وجود Proxy / Nginx.
    """

    x_forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


# ==========================================
# EVALUATION DAYS
# ==========================================

def is_evaluation_day(check_date=None):
    """
    تحديد هل اليوم مسموح فيه إنشاء التقييمات أم لا.

    أيام التقييم:
    السبت
    الأحد
    الاثنين
    الثلاثاء
    الأربعاء

    أيام إغلاق التقييم:
    الخميس
    الجمعة

    weekday():
    الاثنين = 0
    الثلاثاء = 1
    الأربعاء = 2
    الخميس = 3
    الجمعة = 4
    السبت = 5
    الأحد = 6
    """

    if check_date is None:
        check_date = date.today()

    return check_date.weekday() in [
        5,  # السبت
        6,  # الأحد
        0,  # الاثنين
        1,  # الثلاثاء
        2,  # الأربعاء
    ]


# ==========================================
# GET EVALUATION WEEK
# ==========================================

def get_evaluation_week_start(check_date=None):
    """
    إرجاع تاريخ بداية أسبوع التقييم.

    أسبوع التقييم يبدأ يوم السبت
    وينتهي يوم الأربعاء.

    الخميس والجمعة يعتبران فترة إغلاق
    مرتبطة بالأسبوع السابق.

    مثال:

    السبت 8
    الأحد 9
    الاثنين 10
    الثلاثاء 11
    الأربعاء 12

    كلهم لهم نفس بداية الأسبوع:
    السبت 8
    """

    if check_date is None:
        check_date = date.today()

    weekday = check_date.weekday()

    # السبت = 5
    days_from_saturday = (weekday - 5) % 7

    return check_date - timedelta(
        days=days_from_saturday
    )


def get_evaluation_week_number(check_date=None):
    """
    إرجاع رقم أسبوع التقييم.

    الأسبوع يبدأ يوم السبت.

    نستخدم رقم الأسبوع الخاص ببداية
    أسبوع التقييم.
    """

    week_start = get_evaluation_week_start(
        check_date
    )

    return week_start.isocalendar().week


# ==========================================
# CALCULATE EMPLOYEE POINTS
# ==========================================

def calculate_employee_points(user_id):
    """
    حساب نقاط الموظف بناءً على:

    1. متوسط التقييمات = 70%
    2. نسبة الحضور = 30%
    3. خصم التأخير

    PRESENT و LATE يعتبران حضوراً.
    """

    try:
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        return Decimal("0.00")

    # ======================================
    # متوسط التقييمات
    # ======================================

    evaluation_avg = (
        Evaluation.objects
        .filter(
            evaluated_employee=user
        )
        .aggregate(
            avg=Avg("total_score")
        )
        .get("avg")
    )

    if evaluation_avg is None:
        evaluation_avg = Decimal("0.00")
    else:
        evaluation_avg = Decimal(
            str(evaluation_avg)
        )

    # ======================================
    # الحضور
    # ======================================

    attendance_qs = Attendance.objects.filter(
        user=user
    )

    attendance_total = attendance_qs.count()

    attendance_present = attendance_qs.filter(
        status__in=[
            "PRESENT",
            "LATE",
        ]
    ).count()

    attendance_percentage = Decimal("0.00")

    if attendance_total > 0:
        attendance_percentage = (
            Decimal(attendance_present)
            / Decimal(attendance_total)
        ) * Decimal("100")

    # ======================================
    # التأخير
    # ======================================

    late_count = attendance_qs.filter(
        status="LATE"
    ).count()

    # خصم 0.5 نقطة لكل يوم تأخير

    late_penalty = (
        Decimal(late_count)
        * Decimal("0.50")
    )

    # ======================================
    # المعادلة النهائية
    # ======================================

    evaluation_points = (
        evaluation_avg
        * Decimal("0.70")
    )

    attendance_points = (
        attendance_percentage
        * Decimal("0.30")
    )

    points = (
        evaluation_points
        + attendance_points
        - late_penalty
    )

    # منع النقاط من أن تصبح سالبة

    if points < Decimal("0.00"):
        points = Decimal("0.00")

    # تقريب إلى منزلتين عشريتين

    points = points.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return points


# ==========================================
# CALCULATE ATTENDANCE STATUS
# ==========================================

def calculate_attendance_status(check_in_time):
    """
    تحديد حالة الحضور بناءً على وقت الحضور
    الموجود في CompanySetting.

    النتيجة:
    PRESENT أو LATE
    """

    if not check_in_time:
        return "PRESENT"

    setting = (
        CompanySetting.objects
        .order_by("id")
        .first()
    )

    if not setting:
        return "PRESENT"

    if check_in_time > setting.attendance_time:
        return "LATE"

    return "PRESENT"


# ==========================================
# CALCULATE LATE MINUTES
# ==========================================

def calculate_late_minutes(check_in_time):
    """
    حساب عدد دقائق التأخير.
    """

    if not check_in_time:
        return 0

    setting = (
        CompanySetting.objects
        .order_by("id")
        .first()
    )

    if not setting:
        return 0

    if check_in_time <= setting.attendance_time:
        return 0

    check_in_minutes = (
        check_in_time.hour * 60
        + check_in_time.minute
    )

    attendance_minutes = (
        setting.attendance_time.hour * 60
        + setting.attendance_time.minute
    )

    late_minutes = (
        check_in_minutes
        - attendance_minutes
    )

    return max(late_minutes, 0)


# ==========================================
# CHECK USER ROLE
# ==========================================

def has_role(user, roles):
    """
    فحص صلاحية المستخدم.

    مثال:

    has_role(
        request.user,
        ["ADMIN", "BRANCH_MANAGER"]
    )
    """

    if not user or not user.is_authenticated:
        return False

    return user.role in roles


# ==========================================
# GET USER BRANCH
# ==========================================

def get_user_branch(user):
    """
    إرجاع فرع المستخدم.
    """

    if not user or not user.is_authenticated:
        return None

    return user.branch


# ==========================================
# IS ADMIN
# ==========================================

def is_admin(user):
    """
    التحقق من أن المستخدم Admin.
    """

    if not user or not user.is_authenticated:
        return False

    return user.role == "ADMIN"


# ==========================================
# IS BRANCH MANAGER
# ==========================================

def is_branch_manager(user):
    """
    التحقق من أن المستخدم مدير فرع.
    """

    if not user or not user.is_authenticated:
        return False

    return user.role == "BRANCH_MANAGER"


# ==========================================
# IS ADMIN OR BRANCH MANAGER
# ==========================================

def is_admin_or_branch_manager(user):
    """
    التحقق من Admin أو Branch Manager.
    """

    if not user or not user.is_authenticated:
        return False

    return user.role in [
        "ADMIN",
        "BRANCH_MANAGER",
    ]

