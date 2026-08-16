from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import (
    Branch,
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
    Company, # تأكد من استيراد موديل Company هنا
)

User = get_user_model()


# =========================================================
# BRANCH SERIALIZER
# =========================================================

class BranchSerializer(serializers.ModelSerializer):

    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = [
            "id",
            "code",
            "name",
            "location",
            "is_active",
            "employee_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
            "employee_count",
        ]

    def get_employee_count(self, obj):
        return obj.employees.count()


# =========================================================
# USER SERIALIZER (Updated with company_name & branch_name support)
# =========================================================
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
    )

    # حقول إضافية لاستقبال أسماء الشركة والفرع النصية المرسلة من الواجهة الأمامية
    company_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    branch_name = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    # اسم الفرع للعرض بس (read-only) - بيرجع اسم الفرع كـ String وليس الـ ID
    branch_name_display = serializers.CharField(
        source="branch.name",
        read_only=True,
        allow_null=True
    )

    managed_branch_names = serializers.SerializerMethodField()

    # الصلاحيات الخاصة بالمستخدم
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "password",

            "first_name",
            "last_name",

            "employee_code",
            "phone",

            "role",

            "company",             
            "company_name",          # ✅ مضاف حديثاً للاستقبال من الفرونت
            "branch",
            "branch_name",           # ✅ مضاف حديثاً للاستقبال من الفرونت
            "branch_name_display",   # اسم الفرع للعرض (read)

            "managed_branches",
            "managed_branch_names",

            "groups",
            "user_permissions",
            "permissions",

            "is_active",
            "is_staff",
            "is_superuser",

            "points",

            "profile_pic",
            "dark_mode",

            "last_login",
            "last_login_ip",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "company",             
            "points",
            "last_login",
            "last_login_ip",
            "created_at",
            "updated_at",
            "permissions",
            "branch_name_display",
            "managed_branch_names",
        ]

        extra_kwargs = {
            "branch": {"required": False, "allow_null": True},
        }

    def get_managed_branch_names(self, obj):
        return list(
            obj.managed_branches.values_list(
                "name",
                flat=True
            )
        )

    def get_permissions(self, obj):
        """
        إرجاع كل الصلاحيات الفعلية للمستخدم.
        """
        permissions = obj.get_all_permissions()
        return sorted(list(permissions))

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        
        # استخراج أسماء الشركة والفرع المرسلة نصياً من الواجهة الأمامية
        company_name_input = validated_data.pop("company_name", None)
        branch_name_input = validated_data.pop("branch_name", None)

        # ✅ الحقول دي Many-to-Many، لازم تتشال قبل الإنشاء
        managed_branches = validated_data.pop("managed_branches", None)
        groups = validated_data.pop("groups", None)
        user_permissions = validated_data.pop("user_permissions", None)

        request = self.context.get("request")
        
        # 1. تحديد الشركة (إما بالاسم المدخل أو من المدير المسجل)
        if company_name_input and company_name_input.strip():
            company_obj, _ = Company.objects.get_or_create(name=company_name_input.strip())
            validated_data["company"] = company_obj
        elif request and hasattr(request, "user") and request.user.is_authenticated:
            if not request.user.is_superuser and hasattr(request.user, "company") and request.user.company:
                validated_data["company"] = request.user.company

        # 2. تحديد أو إنشاء الفرع وربطه بالشركة
        if branch_name_input and branch_name_input.strip():
            target_company = validated_data.get("company")
            if target_company:
                branch_obj, _ = Branch.objects.get_or_create(
                    name=branch_name_input.strip(), 
                    company=target_company
                )
                validated_data["branch"] = branch_obj

        validated_data['is_active'] = True

        user = User.objects.create(
            **validated_data
        )

        if password:
            user.set_password(password)
            user.save(
                update_fields=["password"]
            )

        # ✅ الحقول الـ M2M بتتظبط بعد إنشاء اليوزر مش وقت الإنشاء
        if managed_branches:
            user.managed_branches.set(managed_branches)

        if groups:
            user.groups.set(groups)

        if user_permissions:
            user.user_permissions.set(user_permissions)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop(
            "password",
            None
        )

        company_name_input = validated_data.pop("company_name", None)
        branch_name_input = validated_data.pop("branch_name", None)

        managed_branches = validated_data.pop("managed_branches", None)
        groups = validated_data.pop("groups", None)
        user_permissions = validated_data.pop("user_permissions", None)

        request = self.context.get("request")
        
        # معالجة تعديل الشركة
        if company_name_input and company_name_input.strip():
            company_obj, _ = Company.objects.get_or_create(name=company_name_input.strip())
            validated_data["company"] = company_obj
        elif request and hasattr(request, "user") and request.user.is_authenticated:
            if not request.user.is_superuser:
                validated_data.pop("company", None) # نحافظ على شركة الموظف الأصلية

        # معالجة تعديل الفرع
        if branch_name_input and branch_name_input.strip():
            current_company = validated_data.get("company", instance.company)
            if current_company:
                branch_obj, _ = Branch.objects.get_or_create(
                    name=branch_name_input.strip(), 
                    company=current_company
                )
                validated_data["branch"] = branch_obj

        for attr, value in validated_data.items():
            setattr(
                instance,
                attr,
                value
            )

        if password:
            instance.set_password(password)

        instance.save()

        if managed_branches is not None:
            instance.managed_branches.set(managed_branches)

        if groups is not None:
            instance.groups.set(groups)

        if user_permissions is not None:
            instance.user_permissions.set(user_permissions)

        return instance
# =========================================================
# EVALUATION SERIALIZER
# =========================================================

class EvaluationSerializer(serializers.ModelSerializer):

    evaluator_name = serializers.CharField(
        source="evaluator.username",
        read_only=True,
    )

    employee_name = serializers.CharField(
        source="evaluated_employee.username",
        read_only=True,
    )

    employee_branch = serializers.CharField(
        source="evaluated_employee.branch.name",
        read_only=True,
    )

    class Meta:
        model = Evaluation

        fields = [
            "id",

            "evaluator",
            "evaluator_name",

            "evaluated_employee",
            "employee_name",
            "employee_branch",

            "criteria_dealing",
            "criteria_accuracy",
            "criteria_honesty",
            "criteria_work_quality",

            "total_score",

            "evaluation_type",
            "week_number",
            "comment",

            "created_at",
        ]

        read_only_fields = [
            "evaluator",
            "evaluator_name",
            "employee_name",
            "employee_branch",
            "total_score",
            "created_at",
        ]

    def validate(self, attrs):

        criteria_fields = [
            "criteria_dealing",
            "criteria_accuracy",
            "criteria_honesty",
            "criteria_work_quality",
        ]

        for field in criteria_fields:

            value = attrs.get(field)

            if value is not None and (
                value < 0 or value > 100
            ):
                raise serializers.ValidationError({
                    field: "يجب أن تكون القيمة بين 0 و100."
                })

        return attrs


# =========================================================
# BRANCH EVALUATION SERIALIZER
# =========================================================

class BranchEvaluationSerializer(
    serializers.ModelSerializer
):

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
    )

    evaluator_name = serializers.CharField(
        source="evaluator.username",
        read_only=True,
    )

    class Meta:
        model = BranchEvaluation

        fields = [
            "id",

            "branch",
            "branch_name",

            "evaluator",
            "evaluator_name",

            "employees_score",
            "admin_score",
            "total_branch_score",

            "week_number",

            "created_at",
        ]

        read_only_fields = [
            "evaluator",
            "evaluator_name",
            "branch_name",
            "total_branch_score",
            "created_at",
        ]

    def validate(self, attrs):

        for field in [
            "employees_score",
            "admin_score",
        ]:

            value = attrs.get(field)

            if value is not None and (
                value < 0 or value > 100
            ):
                raise serializers.ValidationError({
                    field: "يجب أن تكون القيمة بين 0 و100."
                })

        return attrs


# =========================================================
# PRODUCT SERIALIZER
# =========================================================

class ProductSerializer(serializers.ModelSerializer):

    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = [
            "id",
            "product_name",
            "price",

            "offer_price",
            "offer_description",

            "final_price",

            "image",
            "is_offer_active",

            "updated_at",
        ]

        read_only_fields = [
            "updated_at",
            "final_price",
        ]

    def get_final_price(self, obj):

        if (
            obj.is_offer_active
            and obj.offer_price is not None
        ):
            return obj.offer_price

        return obj.price


# =========================================================
# NOTIFICATION SERIALIZER
# =========================================================

class NotificationSerializer(
    serializers.ModelSerializer
):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = Notification

        fields = [
            "id",

            "user",
            "username",

            "type",
            "title",
            "message",

            "is_read",
            "read_at",

            "link",

            "created_at",
        ]

        read_only_fields = [
            "created_at",
            "read_at",
            "username",
        ]


# =========================================================
# ATTENDANCE SERIALIZER
# =========================================================

class AttendanceSerializer(
    serializers.ModelSerializer
):

    employee_name = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    employee_code = serializers.CharField(
        source="user.employee_code",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="user.branch.name",
        read_only=True,
    )

    class Meta:
        model = Attendance

        fields = [
            "id",

            "user",
            "employee_name",
            "employee_code",
            "branch_name",

            "date",

            "check_in_time",
            "check_out_time",

            "check_in_ip",
            "check_out_ip",

            "late_minutes",
            "status",

            "created_at",
        ]

        read_only_fields = [
            "employee_name",
            "employee_code",
            "branch_name",
            "created_at",
        ]


# =========================================================
# MESSAGE SERIALIZER
# =========================================================

class MessageSerializer(
    serializers.ModelSerializer
):

    sender_name = serializers.CharField(
        source="sender.username",
        read_only=True,
    )

    receiver_name = serializers.CharField(
        source="receiver.username",
        read_only=True,
    )

    class Meta:
        model = Message

        fields = [
            "id",

            "sender",
            "sender_name",

            "receiver",
            "receiver_name",

            "receiver_group",

            "subject",
            "message",

            "is_read",

            "created_at",
        ]

        read_only_fields = [
            "sender",
            "sender_name",
            "receiver_name",
            "is_read",
            "created_at",
        ]

    def validate(self, attrs):

        receiver = attrs.get("receiver")
        receiver_group = attrs.get(
            "receiver_group"
        )

        if not receiver and not receiver_group:
            raise serializers.ValidationError(
                "يجب تحديد مستلم أو مجموعة مستلمين."
            )

        if receiver and receiver_group:
            raise serializers.ValidationError(
                "اختر مستلمًا أو مجموعة مستلمين، وليس الاثنين معًا."
            )

        return attrs


# =========================================================
# BACKUP SERIALIZER
# =========================================================

class BackupSerializer(
    serializers.ModelSerializer
):

    creator_name = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )

    class Meta:
        model = Backup

        fields = [
            "id",

            "file_name",
            "file_size",

            "created_by",
            "creator_name",

            "created_at",
        ]

        read_only_fields = [
            "file_name",
            "file_size",
            "created_by",
            "creator_name",
            "created_at",
        ]


# =========================================================
# WEEKLY RANKING SERIALIZER
# =========================================================

class WeeklyRankingSerializer(
    serializers.ModelSerializer
):

    employee_name = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    employee_code = serializers.CharField(
        source="user.employee_code",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="user.branch.name",
        read_only=True,
    )

    class Meta:
        model = WeeklyRanking

        fields = [
            "id",

            "user",
            "employee_name",
            "employee_code",
            "branch_name",

            "week_number",
            "rank_position",
            "reward_amount",

            "created_at",
        ]

        read_only_fields = [
            "employee_name",
            "employee_code",
            "branch_name",
            "created_at",
        ]


# =========================================================
# REWARD SERIALIZER
# =========================================================

class RewardSerializer(
    serializers.ModelSerializer
):

    employee_name = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    employee_code = serializers.CharField(
        source="user.employee_code",
        read_only=True,
    )

    branch_name = serializers.CharField(
        source="user.branch.name",
        read_only=True,
    )

    class Meta:
        model = Reward

        fields = [
            "id",

            "user",
            "employee_name",
            "employee_code",
            "branch_name",

            "week_number",

            "amount",
            "is_paid",

            "created_at",
        ]

        read_only_fields = [
            "employee_name",
            "employee_code",
            "branch_name",
            "created_at",
        ]


# =========================================================
# COMPANY SETTINGS SERIALIZER
# =========================================================

class CompanySettingSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = CompanySetting

        fields = [
            "id",

            "company_name",
            "attendance_time",

            "backup_enabled",
            "backup_days",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]


# =========================================================
# ACTIVITY LOG SERIALIZER
# =========================================================

class ActivityLogSerializer(
    serializers.ModelSerializer
):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    employee_code = serializers.CharField(
        source="user.employee_code",
        read_only=True,
    )

    class Meta:
        model = ActivityLog

        fields = [
            "id",

            "user",
            "username",
            "employee_code",

            "action",
            "ip_address",
            "user_agent",

            "created_at",
        ]

        read_only_fields = [
            "user",
            "username",
            "employee_code",
            "action",
            "ip_address",
            "user_agent",
            "created_at",
        ]
