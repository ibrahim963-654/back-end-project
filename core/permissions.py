from rest_framework.permissions import BasePermission


class IsAuthenticatedAndHasPermission(BasePermission):
    """
    صلاحيات مبنية على Django permissions.

    مثال:
    core.view_product
    core.add_product
    core.change_product
    core.delete_product
    """

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        # Superuser له كل الصلاحيات
        if request.user.is_superuser:
            return True

        permission = self.get_permission(request, view)

        if not permission:
            return False

        return request.user.has_perm(permission)

    def get_permission(self, request, view):

        model = getattr(view, "permission_model", None)

        if not model:
            return None

        action = getattr(view, "action", None)

        if action == "list":
            action = "view"

        elif action == "retrieve":
            action = "view"

        elif action == "create":
            action = "add"

        elif action in ["update", "partial_update"]:
            action = "change"

        elif action == "destroy":
            action = "delete"

        elif action == "read":
            action = "view"

        elif request.method == "GET":
            action = "view"

        elif request.method == "POST":
            action = "add"

        elif request.method in ["PUT", "PATCH"]:
            action = "change"

        elif request.method == "DELETE":
            action = "delete"

        else:
            return None

        return f"{model._meta.app_label}.{action}_{model._meta.model_name}"


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == "ADMIN"
            )
        )


class IsBranchManagerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if user.role == "ADMIN":
            return True

        if user.role == "BRANCH_MANAGER":
            return True

        return False


class IsAdminOrPermission(BasePermission):
    """
    يسمح للـ ADMIN أو المستخدم الذي يمتلك
    الصلاحية المطلوبة.
    """

    permission_model = None

    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if user.role == "ADMIN":
            return True

        model = getattr(
            view,
            "permission_model",
            self.permission_model
        )

        if not model:
            return False

        action = getattr(view, "action", None)

        if action in ["list", "retrieve"]:
            permission = "view"

        elif action == "create":
            permission = "add"

        elif action in ["update", "partial_update"]:
            permission = "change"

        elif action == "destroy":
            permission = "delete"

        elif request.method == "GET":
            permission = "view"

        elif request.method == "POST":
            permission = "add"

        elif request.method in ["PUT", "PATCH"]:
            permission = "change"

        elif request.method == "DELETE":
            permission = "delete"

        else:
            return False

        codename = (
            f"{permission}_"
            f"{model._meta.model_name}"
        )

        full_permission = (
            f"{model._meta.app_label}."
            f"{codename}"
        )

        return user.has_perm(full_permission)

from django.utils import timezone
from rest_framework.permissions import BasePermission


class IsVotingDay(BasePermission):
    message = "التصويتات متاحة من السبت إلى الأربعاء فقط."

    def has_permission(self, request, view):
        # السماح للأدمن دائمًا
        if request.user.is_authenticated and request.user.role == "ADMIN":
            return True

        # Python:
        # Monday = 0
        # Tuesday = 1
        # Wednesday = 2
        # Thursday = 3
        # Friday = 4
        # Saturday = 5
        # Sunday = 6

        return timezone.localdate().weekday() in [5, 6, 0, 1, 2]