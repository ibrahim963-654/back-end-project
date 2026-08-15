from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from core.models import (
    Company,
    Branch,
    User,
    Evaluation,
    BranchEvaluation,
    Product,
    Notification,
    Attendance,
    Message,
    Backup,
    WeeklyRanking,
    Reward,
    CompanySetting,
    ActivityLog,
)

# --- BaseAdmin للعزل الأمني ---
class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.company:
            return qs.filter(company=request.user.company)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if not obj.company and request.user.company:
            obj.company = request.user.company
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "company":
            kwargs["queryset"] = Company.objects.filter(id=request.user.company_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# =========================================================
# COMPANY
# =========================================================

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subdomain", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "subdomain")
    ordering = ("name",)

# =========================================================
# BRANCH
# =========================================================

@admin.register(Branch)
class BranchAdmin(BaseAdmin):
    list_display = ("id", "company", "code", "name", "location", "is_active", "created_at", "updated_at")
    list_filter = ("company", "is_active")
    search_fields = ("code", "name", "location")
    autocomplete_fields = ("company",)
    ordering = ("name",)

# =========================================================
# USER
# =========================================================

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "username", "company", "employee_code", "first_name", "last_name", "role", "branch", "points", "is_active", "last_login", "created_at")
    list_filter = ("company", "role", "branch", "is_active", "is_staff", "is_superuser", "dark_mode")
    search_fields = ("username", "employee_code", "first_name", "last_name", "email", "phone")
    ordering = ("username",)
    autocomplete_fields = ("company", "branch", "managed_branches")
    readonly_fields = ("last_login", "date_joined", "last_login_ip", "created_at", "updated_at")
    fieldsets = (
        ("بيانات الدخول", {"fields": ("username", "password")}),
        ("البيانات الشخصية", {"fields": ("company", "first_name", "last_name", "email", "phone", "employee_code", "profile_pic")}),
        ("بيانات الموظف", {"fields": ("role", "branch", "managed_branches", "points", "dark_mode")}),
        ("الصلاحيات", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("معلومات النظام", {"fields": ("last_login", "date_joined", "last_login_ip", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        ("إنشاء مستخدم", {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "company", "first_name", "last_name", "email", "employee_code", "phone", "role", "branch", "managed_branches", "is_active", "is_staff", "is_superuser"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(company=request.user.company)

# =========================================================
# EVALUATION
# =========================================================

@admin.register(Evaluation)
class EvaluationAdmin(BaseAdmin):
    list_display = ("id", "company", "evaluator", "evaluated_employee", "evaluation_type", "total_score", "year", "week_number", "created_at")
    list_filter = ("company", "evaluation_type", "year", "week_number")
    search_fields = ("evaluator__username", "evaluated_employee__username", "comment")
    autocomplete_fields = ("company", "evaluator", "evaluated_employee")
    readonly_fields = ("total_score", "created_at")
    ordering = ("-created_at",)

# =========================================================
# BRANCH EVALUATION
# =========================================================

@admin.register(BranchEvaluation)
class BranchEvaluationAdmin(BaseAdmin):
    list_display = ("id", "company", "branch", "evaluator", "employees_score", "admin_score", "total_branch_score", "year", "week_number", "created_at")
    list_filter = ("company", "branch", "year", "week_number")
    search_fields = ("branch__name", "branch__code", "evaluator__username")
    autocomplete_fields = ("company", "branch", "evaluator")
    readonly_fields = ("total_branch_score", "created_at")
    ordering = ("-created_at",)

# =========================================================
# PRODUCT
# =========================================================

@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ("id", "company", "product_name", "price", "offer_price", "is_offer_active", "updated_at")
    list_filter = ("company", "is_offer_active", "updated_at")
    search_fields = ("product_name", "offer_description")
    autocomplete_fields = ("company",)
    ordering = ("product_name",)

# =========================================================
# NOTIFICATION
# =========================================================

@admin.register(Notification)
class NotificationAdmin(BaseAdmin):
    list_display = ("id", "company", "user", "type", "title", "is_read", "read_at", "created_at")
    list_filter = ("company", "type", "is_read", "created_at")
    search_fields = ("user__username", "title", "message")
    autocomplete_fields = ("company", "user")
    readonly_fields = ("created_at", "read_at")
    ordering = ("-created_at",)

# =========================================================
# ATTENDANCE
# =========================================================

@admin.register(Attendance)
class AttendanceAdmin(BaseAdmin):
    list_display = ("id", "company", "user", "date", "status", "check_in_time", "check_out_time", "late_minutes", "check_in_ip", "check_out_ip")
    list_filter = ("company", "status", "date")
    search_fields = ("user__username", "user__employee_code", "user__branch__name")
    autocomplete_fields = ("company", "user")
    readonly_fields = ("created_at",)
    date_hierarchy = "date"
    ordering = ("-date", "-check_in_time")

# =========================================================
# MESSAGE
# =========================================================

@admin.register(Message)
class MessageAdmin(BaseAdmin):
    list_display = ("id", "company", "sender", "receiver", "receiver_group", "subject", "is_read", "created_at")
    list_filter = ("company", "receiver_group", "is_read", "created_at")
    search_fields = ("sender__username", "receiver__username", "subject", "message")
    autocomplete_fields = ("company", "sender", "receiver")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

# =========================================================
# BACKUP
# =========================================================

@admin.register(Backup)
class BackupAdmin(BaseAdmin):
    list_display = ("id", "company", "file_name", "file_size", "created_by", "created_at")
    list_filter = ("company", "created_at")
    search_fields = ("file_name", "created_by__username")
    autocomplete_fields = ("company", "created_by")
    readonly_fields = ("file_name", "file_size", "created_by", "created_at")
    ordering = ("-created_at",)

# =========================================================
# WEEKLY RANKING
# =========================================================

@admin.register(WeeklyRanking)
class WeeklyRankingAdmin(BaseAdmin):
    list_display = ("id", "company", "user", "year", "week_number", "rank_position", "reward_amount", "created_at")
    list_filter = ("company", "year", "week_number", "rank_position")
    search_fields = ("user__username", "user__employee_code")
    autocomplete_fields = ("company", "user")
    readonly_fields = ("created_at",)
    ordering = ("year", "week_number", "rank_position")

# =========================================================
# REWARD
# =========================================================

@admin.register(Reward)
class RewardAdmin(BaseAdmin):
    list_display = ("id", "company", "user", "year", "week_number", "amount", "is_paid", "created_at")
    list_filter = ("company", "year", "week_number", "is_paid", "created_at")
    search_fields = ("user__username", "user__employee_code")
    autocomplete_fields = ("company", "user")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

# =========================================================
# COMPANY SETTINGS
# =========================================================

@admin.register(CompanySetting)
class CompanySettingAdmin(BaseAdmin):
    list_display = ("id", "company", "company_name", "attendance_time", "backup_enabled", "backup_days", "created_at", "updated_at")
    list_filter = ("company", "backup_enabled")
    search_fields = ("company_name",)
    autocomplete_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-id",)

# =========================================================
# ACTIVITY LOG
# =========================================================

@admin.register(ActivityLog)
class ActivityLogAdmin(BaseAdmin):
    list_display = ("id", "company", "user", "action", "ip_address", "user_agent", "created_at")
    list_filter = ("company", "created_at")
    search_fields = ("user__username", "action", "ip_address")
    autocomplete_fields = ("company", "user")
    readonly_fields = ("company", "user", "action", "ip_address", "user_agent", "created_at")
    ordering = ("-created_at",)