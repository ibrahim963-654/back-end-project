from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.models import Evaluation, Attendance
from core.utils import calculate_employee_points


# =========================================================
# UPDATE EMPLOYEE POINTS AFTER EVALUATION
# =========================================================

@receiver(
    [post_save, post_delete],
    sender=Evaluation
)
def update_points_after_evaluation(
    sender,
    instance,
    **kwargs
):
    """
    تحديث نقاط الموظف تلقائيًا بعد:
    - إضافة تقييم
    - تعديل تقييم
    - حذف تقييم
    """

    employee = instance.evaluated_employee

    employee.points = calculate_employee_points(
        employee.id
    )

    employee.save(
        update_fields=["points"]
    )


# =========================================================
# UPDATE EMPLOYEE POINTS AFTER ATTENDANCE
# =========================================================

@receiver(
    [post_save, post_delete],
    sender=Attendance
)
def update_points_after_attendance(
    sender,
    instance,
    **kwargs
):
    """
    تحديث نقاط الموظف تلقائيًا بعد:
    - إضافة حضور
    - تعديل حضور
    - حذف حضور
    """

    employee = instance.user

    employee.points = calculate_employee_points(
        employee.id
    )

    employee.save(
        update_fields=["points"]
    )