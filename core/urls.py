from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import (
    # Auth
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ForgotPasswordView,

    # Dashboard
    DashboardStatsView,
    TopFiveEmployeesView,

    # Users
    UserViewSet,

    # Evaluation
    EvaluationViewSet,
    MyEvaluationsView,

    # Products
    ProductViewSet,
    ProductExportExcelView,

    # Notifications
    NotificationViewSet,
    MarkAllNotificationsReadView,
    NotificationCountView,

    # Messages
    MessageViewSet,
    SentMessagesView,
    InboxMessagesView,

    # Attendance
    AttendanceCheckInView,
    AttendanceCheckOutView,
    AttendanceReportView,

    # Reports
    WeeklyPDFReportView,
    MonthlyPDFReportView,
    BranchPDFReportView,

    # Backup
    BackupView,

    # Utility
    ActivityLogViewSet,
    BranchEvaluationViewSet
)

router = DefaultRouter()

# =============================
# ViewSets
# =============================

router.register(
    r'users',
    UserViewSet,
    basename="users"
)

router.register(
    r'employees',
    UserViewSet,
    basename="employees"
)

router.register(
    r'evaluations',
    EvaluationViewSet,
    basename="evaluations"
)

router.register(
    r'votes',
    EvaluationViewSet,
    basename="votes"
)

router.register(
    r'products',
    ProductViewSet,
    basename="products"
)

router.register(
    r'notifications',
    NotificationViewSet,
    basename="notifications"
)

router.register(
    r'messages',
    MessageViewSet,
    basename="messages"
)

router.register(
    r'logs',
    ActivityLogViewSet,
    basename="logs"
)

router.register(
    r'branch-evals',
    BranchEvaluationViewSet,
    basename="branch-evals"
)

urlpatterns = [
    # =============================
    # Authentication
    # =============================
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),

    # =============================
    # Dashboard
    # =============================
    path("dashboard/", DashboardStatsView.as_view()),
    path("dashboard/top5/", TopFiveEmployeesView.as_view()),

    # =============================
    # Evaluations
    # =============================
    path("evaluations/my/", MyEvaluationsView.as_view()),

    # =============================
    # Products
    # =============================
    path("products/export/", ProductExportExcelView.as_view()),

    # =============================
    # Notifications
    # =============================
    path("notifications/mark-all-read/", MarkAllNotificationsReadView.as_view()),
    path("notifications/count/", NotificationCountView.as_view()),

    # =============================
    # Messages
    # =============================
    path("messages/sent/", SentMessagesView.as_view()),
    path("messages/inbox/", InboxMessagesView.as_view()),

    # =============================
    # Attendance
    # =============================
    path("attendance/check-in/", AttendanceCheckInView.as_view()),
    path("attendance/check-out/", AttendanceCheckOutView.as_view()),
    path("attendance/report/", AttendanceReportView.as_view()),

    # =============================
    # Reports
    # =============================
    path("reports/weekly/pdf/", WeeklyPDFReportView.as_view()),
    path("reports/monthly/pdf/", MonthlyPDFReportView.as_view()),
    path("reports/branch/pdf/", BranchPDFReportView.as_view()),

    # =============================
    # Backup
    # =============================
    path("backups/", BackupView.as_view()),

    # Router URLs
    path("", include(router.urls)),
]