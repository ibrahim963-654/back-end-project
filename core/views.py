import os
import subprocess

import openpyxl

from django.conf import settings
from django.contrib.auth import authenticate
from django.db.models import Avg, Q
from django.http import HttpResponse
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from reportlab.pdfgen import canvas

from core.models import (
    User,
    Branch,
    Evaluation,
    BranchEvaluation,
    Product,
    Notification,
    Attendance,
    Company,
    Message,
    Backup,
    WeeklyRanking,
    Reward,
    CompanySetting,
    ActivityLog,
)
from core.permissions import (
    IsAdminUser,
    IsBranchManagerOrAdmin,
    IsAdminOrPermission,
    IsAuthenticatedAndHasPermission,
    IsVotingDay,
)
from core.serializers import (
    BranchSerializer,
    UserSerializer,
    EvaluationSerializer,
    BranchEvaluationSerializer,
    ProductSerializer,
    NotificationSerializer,
    AttendanceSerializer,
    MessageSerializer,
    BackupSerializer,
    WeeklyRankingSerializer,
    RewardSerializer,
    CompanySettingSerializer,
    ActivityLogSerializer,
)

from core.permissions import (
    IsAdminUser,
    IsBranchManagerOrAdmin,
    IsAdminOrPermission,
    IsAuthenticatedAndHasPermission,
)

from core.utils import (
    calculate_employee_points,
    calculate_attendance_status,
    calculate_late_minutes,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_client_ip(request):

    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded:
        return forwarded.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def create_activity_log(request, action):

    ActivityLog.objects.create(
        user=request.user,
        action=action,
        ip_address=get_client_ip(request),
        user_agent=request.META.get(
            "HTTP_USER_AGENT"
        ),
    )


def user_can_access_branch(user, branch):

    if user.is_superuser:
        return True

    if user.role == "ADMIN":
        return True

    if user.role == "REGIONAL":
        return user.managed_branches.filter(
            id=branch.id
        ).exists()

    if user.role == "BRANCH_MANAGER":
        return user.branch_id == branch.id

    return False


# =========================================================
# AUTHENTICATION
# =========================================================

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get(
            "username"
        )

        password = request.data.get(
            "password"
        )

        if not username or not password:

            return Response(
                {
                    "message":
                    "اسم المستخدم وكلمة المرور مطلوبان"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:

            return Response(
                {
                    "message":
                    "بيانات الدخول غير صحيحة"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        user.last_login_ip = get_client_ip(
            request
        )

        user.save(
            update_fields=["last_login_ip"]
        )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh = request.data.get(
            "refresh"
        )

        if not refresh:

            return Response(
                {
                    "message":
                    "Refresh token مطلوب"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            token = RefreshToken(refresh)

            token.blacklist()

            return Response(
                {
                    "message":
                    "تم تسجيل الخروج"
                }
            )

        except Exception:

            return Response(
                {
                    "message":
                    "Token غير صالح"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        return Response(
            UserSerializer(
                request.user
            ).data
        )


# =========================================================
# FORGOT PASSWORD
# =========================================================

class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get(
            "email"
        )

        if not email:

            return Response(
                {
                    "message":
                    "البريد الإلكتروني مطلوب"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message":
                "إذا كان البريد الإلكتروني مسجلًا، سيتم إرسال رابط إعادة كلمة المرور"
            }
        )


# =========================================================
# DASHBOARD
# =========================================================

class DashboardStatsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        user = request.user

        average_evaluation = (
            Evaluation.objects
            .filter(
                evaluated_employee=user
            )
            .aggregate(
                avg=Avg("total_score")
            )
            .get("avg")
            or 0
        )

        data = {
            "points": user.points,

            "average_evaluation":
                average_evaluation,

            "notifications":
                Notification.objects.filter(
                    user=user,
                    is_read=False
                ).count(),

            "attendance":
                Attendance.objects.filter(
                    user=user
                ).count(),
        }

        if (
            user.is_superuser
            or user.role == "ADMIN"
        ):

            data["employees"] = (
                User.objects.count()
            )

            data["branches"] = (
                Branch.objects.count()
            )

            data["evaluations"] = (
                Evaluation.objects.count()
            )

        elif user.role == "BRANCH_MANAGER":

            data["employees"] = (
                User.objects.filter(
                    branch=user.branch
                ).count()
            )

            data["branches"] = 1

            data["evaluations"] = (
                Evaluation.objects.filter(
                    evaluated_employee__branch=
                    user.branch
                ).count()
            )

        return Response(data)


class TopFiveEmployeesView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        queryset = User.objects.all()

        user = request.user

        if user.role == "BRANCH_MANAGER":

            queryset = queryset.filter(
                branch=user.branch
            )

        elif user.role == "REGIONAL":

            queryset = queryset.filter(
                branch__in=
                user.managed_branches.all()
            )

        elif user.role not in [
            "ADMIN",
            "REGIONAL",
            "BRANCH_MANAGER",
        ]:

            queryset = queryset.filter(
                branch=user.branch
            )

        users = (
            queryset
            .select_related("branch")
            .order_by("-points")[:5]
        )

        data = []

        for employee in users:

            data.append(
                {
                    "id": employee.id,

                    "username":
                        employee.username,

                    "points":
                        employee.points,

                    "branch":
                        (
                            employee.branch.name
                            if employee.branch
                            else None
                        ),
                }
            )

        return Response(data)


# =========================================================
# BRANCHES
# =========================================================

class BranchViewSet(viewsets.ModelViewSet):

    serializer_class = BranchSerializer

    permission_classes = [
        IsAdminOrPermission
    ]

    permission_model = Branch

    def get_queryset(self):

        user = self.request.user

        if (
            user.is_superuser
            or user.role == "ADMIN"
        ):

            return Branch.objects.all()

        if user.role == "REGIONAL":

            return Branch.objects.filter(
                id__in=user.managed_branches.values(
                    "id"
                )
            )

        if user.role == "BRANCH_MANAGER":

            return Branch.objects.filter(
                id=user.branch_id
            )

        return Branch.objects.none()

    def perform_create(self, serializer):

        branch = serializer.save()

        create_activity_log(
            self.request,
            f"إضافة الفرع: {branch.name}"
        )

    def perform_update(self, serializer):

        branch = serializer.save()

        create_activity_log(
            self.request,
            f"تعديل الفرع: {branch.name}"
        )

    def perform_destroy(self, instance):

        name = instance.name

        instance.delete()

        create_activity_log(
            self.request,
            f"حذف الفرع: {name}"
        )

# =========================================================
# USERS
# =========================================================
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    permission_classes = [
        IsAdminOrPermission
    ]

    permission_model = User

    def get_queryset(self):
        user = self.request.user
        
        queryset = (
            User.objects
            .select_related("branch", "branch__company")
            .prefetch_related(
                "groups",
                "user_permissions",
                "managed_branches",
            )
            .exclude(is_superuser=True)
            .exclude(role__in=["ADMIN", "MANAGER"])
        )
        if user.is_superuser or user.role == "ADMIN":
            if hasattr(user, 'branch') and user.branch and hasattr(user.branch, 'company'):
                return queryset.filter(branch__company=user.branch.company)
            elif hasattr(user, 'company') and user.company:
                return queryset.filter(company=user.company)
            return queryset
        if user.role == "REGIONAL":
            return queryset.filter(
                branch__in=user.managed_branches.all()
            )
        if user.role == "BRANCH_MANAGER":
            return queryset.filter(
                branch=user.branch
            )
        return queryset.filter(
            id=user.id
        )

   def perform_create(self, serializer):
        try:
            request_data = self.request.data
            company_name = request_data.get('company_name')
            branch_name = request_data.get('branch_name')

            company = None
            branch = None

            if company_name:
                company, _ = Company.objects.get_or_create(name=company_name.strip())

            if branch_name and company:
                branch, _ = Branch.objects.get_or_create(name=branch_name.strip(), company=company)

            create_kwargs = {}
            if company_name:
                create_kwargs['company'] = company
            if branch_name:
                create_kwargs['branch'] = branch

            employee = serializer.save(**create_kwargs)
            display_name = employee.first_name if employee.first_name else employee.username

            create_activity_log(
                self.request,
                f"إضافة مستخدم: {display_name}"
            )
        except Exception as e:
            print(f"CRITICAL ERROR IN CREATE: {str(e)}")
            raise e

    def perform_update(self, serializer):
        request_data = self.request.data
        company_name = request_data.get('company_name')
        branch_name = request_data.get('branch_name')

        company = None
        branch = None

        if company_name:
            company, _ = Company.objects.get_or_create(name=company_name.strip())

        if branch_name and company:
            branch, _ = Branch.objects.get_or_create(name=branch_name.strip(), company=company)

        update_kwargs = {}
        if company_name is not None:
            update_kwargs['company'] = company
        if branch_name is not None:
            update_kwargs['branch'] = branch

        employee = serializer.save(**update_kwargs)

        create_activity_log(
            self.request,
            f"تعديل مستخدم: {employee.username}"
        )

    def perform_destroy(self, instance):
        username = instance.username
        instance.delete()
        create_activity_log(
            self.request,
            f"حذف مستخدم: {username}"
        )

# =========================================================
# USER PERMISSIONS MANAGEMENT
# =========================================================

class UserPermissionsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, user_id):

        if not (
            request.user.is_superuser
            or request.user.role == "ADMIN"
        ):

            return Response(
                {
                    "message":
                    "غير مسموح بإدارة الصلاحيات"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:

            user = User.objects.get(
                id=user_id
            )

        except User.DoesNotExist:

            return Response(
                {
                    "message":
                    "المستخدم غير موجود"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "user_id": user.id,

                "username":
                    user.username,

                "permissions":
                    sorted(
                        user.get_all_permissions()
                    ),

                "direct_permissions": [
                    (
                        permission.content_type
                        .app_label
                        + "."
                        + permission.codename
                    )
                    for permission
                    in user.user_permissions.all()
                ],

                "groups": [
                    group.name
                    for group
                    in user.groups.all()
                ],
            }
        )

    def post(self, request, user_id):

        if not (
            request.user.is_superuser
            or request.user.role == "ADMIN"
        ):

            return Response(
                {
                    "message":
                    "غير مسموح بإدارة الصلاحيات"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:

            user = User.objects.get(
                id=user_id
            )

        except User.DoesNotExist:

            return Response(
                {
                    "message":
                    "المستخدم غير موجود"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        permissions = request.data.get(
            "permissions",
            []
        )

        if not isinstance(
            permissions,
            list
        ):

            return Response(
                {
                    "message":
                    "permissions يجب أن تكون قائمة"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.contrib.auth.models import Permission

        user.user_permissions.clear()

        for permission_name in permissions:

            if "." not in permission_name:

                continue

            app_label, codename = (
                permission_name.split(
                    ".",
                    1
                )
            )

            permission = (
                Permission.objects
                .filter(
                    content_type__app_label=
                    app_label,
                    codename=codename,
                )
                .first()
            )

            if permission:

                user.user_permissions.add(
                    permission
                )

        create_activity_log(
            request,
            f"تعديل صلاحيات المستخدم: "
            f"{user.username}"
        )

        return Response(
            {
                "message":
                "تم تحديث الصلاحيات بنجاح",

                "permissions":
                    sorted(
                        user.get_all_permissions()
                    ),
            }
        )


# =========================================================
# EVALUATIONS
# =========================================================

class EvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationSerializer

    permission_classes = [
        IsAuthenticated,
        IsVotingDay,
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Evaluation.objects.all()

        if user.role == "BRANCH_MANAGER":
            return Evaluation.objects.filter(
                evaluated_employee__branch=user.branch
            )

        return Evaluation.objects.filter(
            evaluated_employee=user
        )

    def perform_create(self, serializer):
        evaluation = serializer.save(
            evaluator=self.request.user
        )

        employee = evaluation.evaluated_employee

        employee.points = calculate_employee_points(
            employee.id
        )

        employee.save(
            update_fields=["points"]
        )

class MyEvaluationsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        evaluations = (
            Evaluation.objects
            .filter(
                evaluated_employee=request.user
            )
            .order_by("-created_at")
        )

        return Response(
            EvaluationSerializer(
                evaluations,
                many=True
            ).data
        )


# =========================================================
# BRANCH EVALUATIONS
# =========================================================

class BranchEvaluationViewSet(viewsets.ModelViewSet):

    serializer_class = BranchEvaluationSerializer

    queryset = BranchEvaluation.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [
                IsAuthenticated(),
                IsVotingDay(),
            ]

        return [
            IsAuthenticated(),
        ]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role == "ADMIN":
            return BranchEvaluation.objects.all()

        if user.role == "REGIONAL":
            return BranchEvaluation.objects.filter(
                branch__in=user.managed_branches.all()
            )

        if user.branch_id:
            return BranchEvaluation.objects.filter(
                branch=user.branch
            )

        return BranchEvaluation.objects.none()

    def perform_create(self, serializer):
        serializer.save(
            evaluator=self.request.user
        )

# =========================================================
# PRODUCTS
# =========================================================

class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    permission_classes = [
        IsAdminOrPermission
    ]

    permission_model = Product

    def get_queryset(self):

        queryset = Product.objects.all()

        search = self.request.query_params.get(
            "search"
        )

        min_price = self.request.query_params.get(
            "min_price"
        )

        max_price = self.request.query_params.get(
            "max_price"
        )

        if search:

            queryset = queryset.filter(
                product_name__icontains=search
            )

        if min_price:

            queryset = queryset.filter(
                price__gte=min_price
            )

        if max_price:

            queryset = queryset.filter(
                price__lte=max_price
            )

        return queryset

    def perform_create(self, serializer):

        product = serializer.save()

        create_activity_log(
            self.request,
            f"إضافة المنتج: "
            f"{product.product_name}"
        )

    def perform_update(self, serializer):

        product = serializer.save()

        create_activity_log(
            self.request,
            f"تعديل المنتج: "
            f"{product.product_name}"
        )

    def perform_destroy(self, instance):

        product_name = (
            instance.product_name
        )

        instance.delete()

        create_activity_log(
            self.request,
            f"حذف المنتج: {product_name}"
        )


# =========================================================
# PRODUCT EXCEL
# =========================================================

class ProductExportExcelView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        if not (
            request.user.is_superuser
            or request.user.has_perm(
                "core.view_product"
            )
        ):

            return Response(
                {
                    "message":
                    "ليس لديك صلاحية تصدير المنتجات"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        workbook = openpyxl.Workbook()

        sheet = workbook.active

        sheet.title = "Products"

        sheet.append(
            [
                "ID",
                "Product Name",
                "Price",
                "Offer Price",
                "Offer Active",
            ]
        )

        for product in Product.objects.all():

            sheet.append(
                [
                    product.id,

                    product.product_name,

                    float(product.price)
                    if product.price is not None
                    else "",

                    float(product.offer_price)
                    if product.offer_price is not None
                    else "",

                    product.is_offer_active,
                ]
            )

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        )

        response[
            "Content-Disposition"
        ] = (
            'attachment; '
            'filename="products.xlsx"'
        )

        workbook.save(response)

        return response


# =========================================================
# NOTIFICATIONS
# =========================================================

class NotificationViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        NotificationSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    http_method_names = [
        "get",
        "patch",
        "post",
    ]

    def get_queryset(self):

        return (
            Notification.objects
            .filter(
                user=self.request.user
            )
            .order_by(
                "-is_read",
                "-created_at"
            )
        )

    def partial_update(
        self,
        request,
        *args,
        **kwargs
    ):

        notification = (
            self.get_object()
        )

        notification.is_read = True

        notification.read_at = (
            timezone.now()
        )

        notification.save(
            update_fields=[
                "is_read",
                "read_at"
            ]
        )

        return Response(
            NotificationSerializer(
                notification
            ).data
        )


class MarkAllNotificationsReadView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).update(
            is_read=True,
            read_at=timezone.now(),
        )

        return Response(
            {
                "message":
                "تم تعليم كل الإشعارات كمقروءة"
            }
        )


class NotificationCountView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        count = (
            Notification.objects
            .filter(
                user=request.user,
                is_read=False,
            )
            .count()
        )

        return Response(
            {
                "unread_count": count
            }
        )


# =========================================================
# MESSAGES
# =========================================================

class MessageViewSet(viewsets.ModelViewSet):

    serializer_class = MessageSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        return (
            Message.objects
            .filter(
                Q(receiver=user)
                |
                Q(sender=user)
            )
            .order_by("-created_at")
        )

    def perform_create(self, serializer):

        message = serializer.save(
            sender=self.request.user
        )

        create_activity_log(
            self.request,
            f"إرسال رسالة: "
            f"{message.subject}"
        )

    def partial_update(
        self,
        request,
        *args,
        **kwargs
    ):

        message = self.get_object()

        if message.receiver != request.user:

            return Response(
                {
                    "message":
                    "غير مسموح بتعديل هذه الرسالة"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        message.is_read = True

        message.save(
            update_fields=["is_read"]
        )

        return Response(
            MessageSerializer(
                message
            ).data
        )


class SentMessagesView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        messages = (
            Message.objects
            .filter(
                sender=request.user
            )
            .order_by("-created_at")
        )

        return Response(
            MessageSerializer(
                messages,
                many=True
            ).data
        )


class InboxMessagesView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        messages = (
            Message.objects
            .filter(
                receiver=request.user
            )
            .order_by("-created_at")
        )

        return Response(
            MessageSerializer(
                messages,
                many=True
            ).data
        )


# =========================================================
# ATTENDANCE
# =========================================================

class AttendanceCheckInView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        user = request.user

        today = timezone.localdate()

        attendance, created = (
            Attendance.objects.get_or_create(
                user=user,
                date=today,
            )
        )

        if attendance.check_in_time:

            return Response(
                {
                    "message":
                    "تم تسجيل الحضور مسبقًا",

                    "time":
                    attendance.check_in_time,
                }
            )

        now = timezone.localtime()

        attendance.check_in_time = (
            now.time()
        )

        attendance.check_in_ip = (
            get_client_ip(request)
        )

        attendance.late_minutes = (
            calculate_late_minutes(
                user,
                now.time()
            )
        )

        attendance.status = (
            calculate_attendance_status(
                attendance.late_minutes
            )
        )

        attendance.save()

        create_activity_log(
            request,
            "تسجيل حضور"
        )

        return Response(
            {
                "message":
                "تم تسجيل الحضور",

                "time":
                attendance.check_in_time,

                "late_minutes":
                attendance.late_minutes,

                "status":
                attendance.status,
            }
        )


class AttendanceCheckOutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        today = timezone.localdate()

        try:

            attendance = (
                Attendance.objects.get(
                    user=request.user,
                    date=today,
                )
            )

        except Attendance.DoesNotExist:

            return Response(
                {
                    "message":
                    "لم يتم تسجيل حضور اليوم"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if attendance.check_out_time:

            return Response(
                {
                    "message":
                    "تم تسجيل الانصراف مسبقًا",

                    "time":
                    attendance.check_out_time,
                }
            )

        now = timezone.localtime()

        attendance.check_out_time = (
            now.time()
        )

        attendance.check_out_ip = (
            get_client_ip(request)
        )

        attendance.save()

        create_activity_log(
            request,
            "تسجيل انصراف"
        )

        return Response(
            {
                "message":
                "تم تسجيل الانصراف",

                "time":
                attendance.check_out_time,
            }
        )


class AttendanceReportView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        user = request.user

        if not (
            user.is_superuser
            or user.role in [
                "ADMIN",
                "BRANCH_MANAGER",
                "REGIONAL",
            ]
            or user.has_perm(
                "core.view_attendance"
            )
        ):

            return Response(
                {
                    "message":
                    "ليس لديك صلاحية عرض الحضور"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        records = (
            Attendance.objects
            .select_related(
                "user",
                "user__branch"
            )
        )

        if user.role == "BRANCH_MANAGER":

            records = records.filter(
                user__branch=user.branch
            )

        elif user.role == "REGIONAL":

            records = records.filter(
                user__branch__in=
                user.managed_branches.all()
            )

        month = request.GET.get(
            "month"
        )

        year = request.GET.get(
            "year"
        )

        user_id = request.GET.get(
            "user_id"
        )

        if year:

            records = records.filter(
                date__year=year
            )

        if month:

            records = records.filter(
                date__month=month
            )

        if user_id:

            records = records.filter(
                user_id=user_id
            )

        data = []

        for item in records:

            data.append(
                {
                    "id": item.id,

                    "employee":
                        item.user.username,

                    "employee_code":
                        item.user.employee_code,

                    "branch":
                        (
                            item.user.branch.name
                            if item.user.branch
                            else None
                        ),

                    "date":
                        item.date,

                    "status":
                        item.status,

                    "check_in":
                        item.check_in_time,

                    "check_out":
                        item.check_out_time,

                    "late_minutes":
                        item.late_minutes,
                }
            )

        return Response(data)


# =========================================================
# WEEKLY RANKING
# =========================================================

class WeeklyRankingViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        WeeklyRankingSerializer
    )

    permission_classes = [
        IsAdminOrPermission
    ]

    permission_model = WeeklyRanking

    def get_queryset(self):

        user = self.request.user

        queryset = (
            WeeklyRanking.objects
            .select_related(
                "user",
                "user__branch"
            )
        )

        if (
            user.is_superuser
            or user.role == "ADMIN"
        ):

            return queryset

        if user.role == "REGIONAL":

            return queryset.filter(
                user__branch__in=
                user.managed_branches.all()
            )

        if user.role == "BRANCH_MANAGER":

            return queryset.filter(
                user__branch=user.branch
            )

        return queryset.filter(
            user=user
        )


# =========================================================
# REWARDS
# =========================================================

class RewardViewSet(viewsets.ModelViewSet):

    serializer_class = RewardSerializer

    permission_classes = [
        IsAdminOrPermission
    ]

    permission_model = Reward

    def get_queryset(self):

        user = self.request.user

        queryset = (
            Reward.objects
            .select_related(
                "user",
                "user__branch"
            )
        )

        if (
            user.is_superuser
            or user.role == "ADMIN"
        ):

            return queryset

        if user.role == "REGIONAL":

            return queryset.filter(
                user__branch__in=
                user.managed_branches.all()
            )

        if user.role == "BRANCH_MANAGER":

            return queryset.filter(
                user__branch=user.branch
            )

        return queryset.filter(
            user=user
        )


# =========================================================
# COMPANY SETTINGS
# =========================================================

class CompanySettingViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        CompanySettingSerializer
    )

    permission_classes = [
        IsAdminOrPermission
    ]

    permission_model = CompanySetting

    def get_queryset(self):

        return CompanySetting.objects.all()

    def perform_create(self, serializer):

        setting = serializer.save()

        create_activity_log(
            self.request,
            "إضافة إعدادات الشركة"
        )

    def perform_update(self, serializer):

        setting = serializer.save()

        create_activity_log(
            self.request,
            "تعديل إعدادات الشركة"
        )


# =========================================================
# PDF REPORT BASE
# =========================================================

class PDFReportBaseView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def create_pdf(
        self,
        title
    ):

        filename = (
            f"{title}_"
            f"{timezone.localdate()}.pdf"
        )

        os.makedirs(
            settings.MEDIA_ROOT,
            exist_ok=True
        )

        path = os.path.join(
            settings.MEDIA_ROOT,
            filename
        )

        pdf = canvas.Canvas(path)

        pdf.drawString(
            100,
            750,
            title
        )

        pdf.save()

        return filename


class WeeklyPDFReportView(
    PDFReportBaseView
):

    def get(self, request):

        if not (
            request.user.is_superuser
            or request.user.role == "ADMIN"
            or request.user.has_perm(
                "core.view_weeklyranking"
            )
        ):

            return Response(
                {
                    "message":
                    "ليس لديك صلاحية التقرير"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        file = self.create_pdf(
            "weekly_report"
        )

        return Response(
            {
                "file":
                settings.MEDIA_URL + file
            }
        )


class MonthlyPDFReportView(
    PDFReportBaseView
):

    def get(self, request):

        if not (
            request.user.is_superuser
            or request.user.role == "ADMIN"
            or request.user.has_perm(
                "core.view_attendance"
            )
        ):

            return Response(
                {
                    "message":
                    "ليس لديك صلاحية التقرير"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        file = self.create_pdf(
            "monthly_report"
        )

        return Response(
            {
                "file":
                settings.MEDIA_URL + file
            }
        )


class BranchPDFReportView(
    PDFReportBaseView
):

    def get(self, request):

        if not (
            request.user.is_superuser
            or request.user.role == "ADMIN"
            or request.user.has_perm(
                "core.view_branchevaluation"
            )
        ):

            return Response(
                {
                    "message":
                    "ليس لديك صلاحية التقرير"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        file = self.create_pdf(
            "branch_report"
        )

        return Response(
            {
                "file":
                settings.MEDIA_URL + file
            }
        )


# =========================================================
# BACKUP
# =========================================================

class BackupView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        if not (
            request.user.is_superuser
            or request.user.has_perm(
                "core.view_backup"
            )
        ):

            return Response(
                {
                    "message":
                    "ليس لديك صلاحية عرض النسخ الاحتياطية"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        backups = (
            Backup.objects
            .all()
            .order_by("-created_at")[:30]
        )

        return Response(
            BackupSerializer(
                backups,
                many=True
            ).data
        )

    def post(self, request):

        if not (
            request.user.is_superuser
            or request.user.has_perm(
                "core.add_backup"
            )
        ):

            return Response(
                {
                    "message":
                    "ليس لديك صلاحية إنشاء نسخة احتياطية"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        os.makedirs(
            settings.MEDIA_ROOT,
            exist_ok=True
        )

        filename = (
            f"backup_"
            f"{timezone.now().strftime('%Y%m%d_%H%M%S')}"
            ".json"
        )

        path = os.path.join(
            settings.MEDIA_ROOT,
            filename
        )

        try:

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as output_file:

                result = subprocess.run(
                    [
                        "python",
                        "manage.py",
                        "dumpdata",
                    ],
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False,
                )

            if result.returncode != 0:

                return Response(
                    {
                        "message":
                        "فشل إنشاء النسخة الاحتياطية",

                        "error":
                        result.stderr,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as exc:

            return Response(
                {
                    "message":
                    "حدث خطأ أثناء إنشاء النسخة الاحتياطية",

                    "error":
                    str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        backup = Backup.objects.create(
            file_name=filename,

            file_size=(
                f"{os.path.getsize(path)} bytes"
            ),

            created_by=request.user,
        )

        create_activity_log(
            request,
            "إنشاء نسخة احتياطية"
        )

        return Response(
            BackupSerializer(
                backup
            ).data,
            status=status.HTTP_201_CREATED
        )


# =========================================================
# ACTIVITY LOG
# =========================================================

class ActivityLogViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = (
        ActivityLogSerializer
    )

    permission_classes = [
        IsAdminOrPermission
    ]

    permission_model = ActivityLog

    def get_queryset(self):

        return (
            ActivityLog.objects
            .select_related("user")
            .all()
            .order_by("-created_at")
        )
