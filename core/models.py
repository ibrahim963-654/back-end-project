from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# =========================================================
# COMPANY (الشركة - الجذر الأساسي لنظام Multi-Tenancy)
# =========================================================

class Company(models.Model):
    name = models.CharField(
        "اسم الشركة",
        max_length=255,
        unique=True
    )
    subdomain = models.CharField(
        "النطاق الفرعي أو الكود",
        max_length=100,
        unique=True
    )
    is_active = models.BooleanField(
        "نشطة",
        default=True
    )
    created_at = models.DateTimeField(
        "تاريخ الإنشاء",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "آخر تعديل",
        auto_now=True
    )

    class Meta:
        verbose_name = "شركة"
        verbose_name_plural = "الشركات"
        ordering = ["name"]

    def __str__(self):
        return self.name


# =========================================================
# BRANCH
# =========================================================

class Branch(models.Model):
    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="branches",
        null=True,
        blank=True
    )

    code = models.CharField(
        "كود الفرع",
        max_length=20
    )

    name = models.CharField(
        "اسم الفرع",
        max_length=100
    )

    location = models.CharField(
        "موقع الفرع",
        max_length=255,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        "نشط",
        default=True
    )

    created_at = models.DateTimeField(
        "تاريخ الإنشاء",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "آخر تعديل",
        auto_now=True
    )

    class Meta:
        verbose_name = "فرع"
        verbose_name_plural = "الفروع"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_branch_code_per_company"
            ),
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_branch_name_per_company"
            ),
        ]

    def __str__(self):
        return f"{self.name}"

# =========================================================
# USER
# =========================================================
class User(AbstractUser):
    username = models.CharField(
        "اسم المستخدم الفرعي",
        max_length=150,
        unique=True,
        blank=True
    )

    ROLE_CHOICES = (
        ("ADMIN", "أدمن"),
        ("MANAGER", "مدير"),
        ("REGIONAL", "إقليمي"),
        ("ACCOUNTANT", "محاسب"),
        ("CASHIER", "كاشير"),
        ("SALES", "مبيعات"),
    )

    company = models.ForeignKey(
        'Company',
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users"
    )

    employee_code = models.CharField(
        "كود الموظف",
        max_length=20,
        null=True,
        blank=True
    )

    managed_branches = models.ManyToManyField(
        'Branch',
        blank=True,
        related_name="regional_managers"
    )

    phone = models.CharField(
        "رقم الهاتف",
        max_length=20,
        null=True,
        blank=True
    )

    role = models.CharField(
        "الصلاحية الوظيفية",
        max_length=50,
        choices=ROLE_CHOICES,
        default="SALES"
    )

    branch = models.ForeignKey(
        'Branch',
        verbose_name="الفرع",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

    points = models.DecimalField(
        "النقاط",
        max_digits=7,
        decimal_places=2,
        default=0
    )

    profile_pic = models.ImageField(
        "الصورة الشخصية",
        upload_to="profile_pics/",
        null=True,
        blank=True
    )

    dark_mode = models.BooleanField(
        "الوضع الليلي",
        default=False
    )

    last_login_ip = models.GenericIPAddressField(
        "آخر IP دخول",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        "تاريخ الإنشاء",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "آخر تعديل",
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"user_{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "موظف"
        verbose_name_plural = "الموظفين"
        ordering = ["username"]

    def __str__(self):
        return str(self.first_name or self.username)
# =========================================================
# EVALUATION
# =========================================================

class Evaluation(models.Model):

    EVALUATION_TYPE_CHOICES = (
        ("PEER", "تقييم زملاء"),
        ("ADMIN", "تقييم الإدارة"),
        ("MANAGER", "تقييم مدير الفرع"),
    )

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="evaluations",
        null=True,
        blank=True
    )

    evaluator = models.ForeignKey(
        User,
        verbose_name="المقيم",
        on_delete=models.CASCADE,
        related_name="given_evaluations"
    )

    evaluated_employee = models.ForeignKey(
        User,
        verbose_name="الموظف المقيم",
        on_delete=models.CASCADE,
        related_name="received_evaluations"
    )

    criteria_dealing = models.DecimalField(
        "التعامل",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    criteria_accuracy = models.DecimalField(
        "الدقة",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    criteria_honesty = models.DecimalField(
        "الأمانة",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    criteria_work_quality = models.DecimalField(
        "جودة العمل",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    total_score = models.DecimalField(
        "المجموع النهائي",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    evaluation_type = models.CharField(
        "نوع التقييم",
        max_length=50,
        choices=EVALUATION_TYPE_CHOICES,
        default="PEER"
    )

    year = models.PositiveIntegerField(
        "السنة",
        default=timezone.now().year
    )

    week_number = models.PositiveIntegerField(
        "رقم الأسبوع",
        default=1
    )

    comment = models.TextField(
        "التعليق",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        "تاريخ التقييم",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "تقييم موظف"
        verbose_name_plural = "تقييمات الموظفين"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "evaluator",
                    "evaluated_employee",
                    "year",
                    "week_number",
                ],
                name="unique_employee_evaluation_per_week"
            ),

            models.CheckConstraint(
                condition=~models.Q(
                    evaluator=models.F("evaluated_employee")
                ),
                name="prevent_self_employee_evaluation"
            ),

            models.CheckConstraint(
                condition=models.Q(
                    criteria_dealing__gte=0,
                    criteria_accuracy__gte=0,
                    criteria_honesty__gte=0,
                    criteria_work_quality__gte=0,
                ),
                name="evaluation_scores_not_negative"
            ),
        ]

        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.total_score = (
            self.criteria_dealing +
            self.criteria_accuracy +
            self.criteria_honesty +
            self.criteria_work_quality
        ) / 4

        if not self.year:
            self.year = timezone.localdate().year

        if not self.company and self.evaluator and self.evaluator.company:
            self.company = self.evaluator.company

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.evaluator} -> {self.evaluated_employee}"


# =========================================================
# BRANCH EVALUATION
# =========================================================

class BranchEvaluation(models.Model):

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="branch_evaluations",
        null=True,
        blank=True
    )

    branch = models.ForeignKey(
        Branch,
        verbose_name="الفرع",
        on_delete=models.CASCADE,
        related_name="branch_evaluations"
    )

    evaluator = models.ForeignKey(
        User,
        verbose_name="المقيم",
        on_delete=models.CASCADE,
        related_name="branch_evaluations"
    )

    employees_score = models.DecimalField(
        "تقييم الموظفين",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    admin_score = models.DecimalField(
        "تقييم الإدارة",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    total_branch_score = models.DecimalField(
        "التقييم النهائي للفرع",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    year = models.PositiveIntegerField(
        "السنة",
        default=timezone.now().year
    )

    week_number = models.PositiveIntegerField(
        "رقم الأسبوع",
        default=1
    )

    created_at = models.DateTimeField(
        "تاريخ التقييم",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "تقييم فرع"
        verbose_name_plural = "تقييمات الفروع"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "branch",
                    "evaluator",
                    "year",
                    "week_number",
                ],
                name="unique_branch_evaluation_per_week"
            ),

            models.CheckConstraint(
                condition=models.Q(
                    employees_score__gte=0,
                    admin_score__gte=0,
                ),
                name="branch_scores_not_negative"
            ),
        ]

        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.total_branch_score = (
            self.employees_score +
            self.admin_score
        ) / 2

        if not self.year:
            self.year = timezone.localdate().year

        if not self.company and self.branch and self.branch.company:
            self.company = self.branch.company

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.branch} - الأسبوع {self.week_number}"


# =========================================================
# PRODUCT
# =========================================================

class Product(models.Model):

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )

    product_name = models.CharField(
        "اسم المنتج",
        max_length=200
    )

    price = models.DecimalField(
        "السعر",
        max_digits=10,
        decimal_places=2
    )

    offer_price = models.DecimalField(
        "سعر العرض",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    offer_description = models.TextField(
        "وصف العرض",
        null=True,
        blank=True
    )

    image = models.ImageField(
        "صورة المنتج",
        upload_to="products/",
        null=True,
        blank=True
    )

    is_offer_active = models.BooleanField(
        "العرض فعال",
        default=False
    )

    updated_at = models.DateTimeField(
        "آخر تعديل",
        auto_now=True
    )

    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ["product_name"]

    def __str__(self):
        return self.product_name


# =========================================================
# NOTIFICATION
# =========================================================

class Notification(models.Model):

    TYPE_CHOICES = (
        ("PRICE_UPDATE", "تحديث سعر"),
        ("EVALUATION", "تقييم"),
        ("REWARD", "مكافأة"),
        ("MESSAGE", "رسالة"),
        ("ATTENDANCE", "حضور"),
        ("SYSTEM", "النظام"),
    )

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        User,
        verbose_name="المستخدم",
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    type = models.CharField(
        "نوع الإشعار",
        max_length=50,
        choices=TYPE_CHOICES,
        default="SYSTEM"
    )

    title = models.CharField(
        "العنوان",
        max_length=200
    )

    message = models.TextField(
        "الرسالة"
    )

    is_read = models.BooleanField(
        "تمت القراءة",
        default=False
    )

    read_at = models.DateTimeField(
        "وقت القراءة",
        null=True,
        blank=True
    )

    link = models.CharField(
        "الرابط",
        max_length=255,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        "تاريخ الإنشاء",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "إشعار"
        verbose_name_plural = "الإشعارات"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.company and self.user and self.user.company:
            self.company = self.user.company
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# =========================================================
# ATTENDANCE
# =========================================================

class Attendance(models.Model):

    STATUS_CHOICES = (
        ("PRESENT", "حاضر"),
        ("ABSENT", "غائب"),
        ("LATE", "متأخر"),
    )

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="attendances",
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        User,
        verbose_name="الموظف",
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    date = models.DateField(
        "التاريخ",
        default=timezone.localdate
    )

    check_in_time = models.TimeField(
        "وقت الحضور",
        null=True,
        blank=True
    )

    check_out_time = models.TimeField(
        "وقت الانصراف",
        null=True,
        blank=True
    )

    check_in_ip = models.GenericIPAddressField(
        "IP الحضور",
        null=True,
        blank=True
    )

    check_out_ip = models.GenericIPAddressField(
        "IP الانصراف",
        null=True,
        blank=True
    )

    late_minutes = models.IntegerField(
        "دقائق التأخير",
        default=0
    )

    status = models.CharField(
        "الحالة",
        max_length=20,
        choices=STATUS_CHOICES,
        default="PRESENT"
    )

    created_at = models.DateTimeField(
        "تاريخ التسجيل",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "حضور"
        verbose_name_plural = "سجل الحضور"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_attendance_per_day"
            ),
        ]

        ordering = ["-date", "-check_in_time"]

    def save(self, *args, **kwargs):
        if not self.company and self.user and self.user.company:
            self.company = self.user.company
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.date}"


# =========================================================
# MESSAGE
# =========================================================

class Message(models.Model):

    GROUP_CHOICES = (
        ("ALL", "الجميع"),
        ("ACCOUNTANTS", "المحاسبين"),
        ("CASHIERS", "الكاشير"),
        ("REGIONALS", "المديرين الإقليميين"),
        ("BRANCH_MANAGERS", "مديري الفروع"),
    )

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True
    )

    sender = models.ForeignKey(
        User,
        verbose_name="المرسل",
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    receiver = models.ForeignKey(
        User,
        verbose_name="المستلم",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received_messages"
    )

    receiver_group = models.CharField(
        "مجموعة المستلمين",
        max_length=50,
        choices=GROUP_CHOICES,
        null=True,
        blank=True
    )

    subject = models.CharField(
        "العنوان",
        max_length=255
    )

    message = models.TextField(
        "الرسالة"
    )

    is_read = models.BooleanField(
        "تمت القراءة",
        default=False
    )

    created_at = models.DateTimeField(
        "تاريخ الإرسال",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "رسالة"
        verbose_name_plural = "الرسائل"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.company and self.sender and self.sender.company:
            self.company = self.sender.company
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject


# =========================================================
# BACKUP
# =========================================================

class Backup(models.Model):

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="backups",
        null=True,
        blank=True
    )

    file_name = models.CharField(
        "اسم الملف",
        max_length=255
    )

    file_size = models.CharField(
        "حجم الملف",
        max_length=50,
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        User,
        verbose_name="تم الإنشاء بواسطة",
        on_delete=models.SET_NULL,
        null=True,
        related_name="backups"
    )

    created_at = models.DateTimeField(
        "تاريخ النسخة",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "نسخة احتياطية"
        verbose_name_plural = "النسخ الاحتياطية"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.company and self.created_by and self.created_by.company:
            self.company = self.created_by.company
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name


# =========================================================
# WEEKLY RANKING
# =========================================================

class WeeklyRanking(models.Model):

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="weekly_rankings",
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        User,
        verbose_name="الموظف",
        on_delete=models.CASCADE,
        related_name="weekly_rankings"
    )

    year = models.PositiveIntegerField(
        "السنة",
        default=timezone.now().year
    )

    week_number = models.PositiveIntegerField(
        "رقم الأسبوع"
    )

    rank_position = models.PositiveIntegerField(
        "الترتيب"
    )

    reward_amount = models.DecimalField(
        "قيمة المكافأة",
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        "تاريخ التسجيل",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "ترتيب أسبوعي"
        verbose_name_plural = "الترتيبات الأسبوعية"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "year",
                    "week_number",
                ],
                name="unique_user_weekly_ranking"
            ),

            models.UniqueConstraint(
                fields=[
                    "year",
                    "week_number",
                    "rank_position",
                ],
                name="unique_weekly_rank_position"
            ),
        ]

        ordering = [
            "year",
            "week_number",
            "rank_position",
        ]

    def save(self, *args, **kwargs):
        if not self.company and self.user and self.user.company:
            self.company = self.user.company
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - الأسبوع {self.week_number}"


# =========================================================
# REWARD
# =========================================================

class Reward(models.Model):

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="rewards",
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        User,
        verbose_name="الموظف",
        on_delete=models.CASCADE,
        related_name="rewards"
    )

    year = models.PositiveIntegerField(
        "السنة",
        default=timezone.now().year
    )

    week_number = models.PositiveIntegerField(
        "رقم الأسبوع"
    )

    amount = models.DecimalField(
        "قيمة المكافأة",
        max_digits=10,
        decimal_places=2
    )

    is_paid = models.BooleanField(
        "تم الدفع",
        default=False
    )

    created_at = models.DateTimeField(
        "تاريخ المكافأة",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "مكافأة"
        verbose_name_plural = "المكافآت"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "year",
                    "week_number",
                ],
                name="unique_user_reward_per_week"
            ),
        ]

        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.company and self.user and self.user.company:
            self.company = self.user.company
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.amount}"


# =========================================================
# COMPANY SETTINGS
# =========================================================

class CompanySetting(models.Model):

    company = models.OneToOneField(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="settings",
        null=True,
        blank=True
    )

    company_name = models.CharField(
        "اسم الشركة",
        max_length=200,
        default="الشركة"
    )

    attendance_time = models.TimeField(
        "ميعاد الحضور",
        default="09:00"
    )

    backup_enabled = models.BooleanField(
        "تفعيل النسخ الاحتياطي",
        default=True
    )

    backup_days = models.IntegerField(
        "عدد أيام الاحتفاظ بالنسخ",
        default=30
    )

    created_at = models.DateTimeField(
        "تاريخ الإنشاء",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "آخر تعديل",
        auto_now=True
    )

    class Meta:
        verbose_name = "إعدادات الشركة"
        verbose_name_plural = "إعدادات الشركة"

    def __str__(self):
        return self.company_name


# =========================================================
# ACTIVITY LOG
# =========================================================

class ActivityLog(models.Model):

    company = models.ForeignKey(
        Company,
        verbose_name="الشركة",
        on_delete=models.CASCADE,
        related_name="activity_logs",
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        User,
        verbose_name="المستخدم",
        on_delete=models.SET_NULL,
        null=True,
        related_name="activity_logs"
    )

    action = models.CharField(
        "العملية",
        max_length=255
    )

    ip_address = models.GenericIPAddressField(
        "عنوان IP",
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        "بيانات المتصفح",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        "تاريخ العملية",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "سجل نشاط"
        verbose_name_plural = "سجلات النشاط"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.company and self.user and self.user.company:
            self.company = self.user.company
        super().save(*args, **kwargs)

    def __str__(self):
        return self.action