# ==========================================
# CELERY TASKS
# ==========================================

from celery import shared_task

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from core.models import (
    Backup,
    WeeklyRanking,
    Reward,
    Notification,
)

import subprocess
import os
from datetime import datetime


User = get_user_model()


# ==========================================
# DAILY DATABASE BACKUP
# ==========================================

@shared_task
def daily_backup_task():

    filename = (
        f"backup_"
        f"{datetime.now().strftime('%Y%m%d_%H%M')}"
        ".json"
    )

    path = os.path.join(
        settings.MEDIA_ROOT,
        "backups"
    )

    os.makedirs(
        path,
        exist_ok=True
    )

    file_path = os.path.join(
        path,
        filename
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as backup_file:

        result = subprocess.run(
            [
                "python",
                "manage.py",
                "dumpdata",
            ],
            stdout=backup_file,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    if result.returncode != 0:
        return "Backup Failed"

    Backup.objects.create(
        file_name=filename,
        file_size=(
            f"{os.path.getsize(file_path)} bytes"
        )
    )

    return "Backup Created"


# ==========================================
# WEEKLY RANKING
# ==========================================

@shared_task
def weekly_ranking_task():

    current_week = (
        timezone.localdate().isocalendar().week
    )

    users = (
        User.objects
        .filter(
            is_active=True
        )
        .order_by(
            "-points",
            "id"
        )
    )

    # حذف نتائج الأسبوع الحالية لو المهمة
    # اتنفذت مرة أخرى بالخطأ
    WeeklyRanking.objects.filter(
        week_number=current_week
    ).delete()

    for index, user in enumerate(
        users,
        start=1
    ):

        WeeklyRanking.objects.create(
            user=user,
            week_number=current_week,
            rank_position=index,
            reward_amount=0
        )

    return "Weekly ranking created"


# ==========================================
# WEEKLY REWARD NOTIFICATION
# ==========================================

@shared_task
def weekly_reward_notification_task():

    current_week = (
        timezone.localdate().isocalendar().week
    )

    rankings = (
        WeeklyRanking.objects
        .filter(
            week_number=current_week
        )
        .select_related("user")
        .order_by("rank_position")
    )

    for ranking in rankings:

        user = ranking.user

        Notification.objects.create(
            user=user,
            type="REWARD",
            title="ترتيب الأسبوع",
            message=(
                f"أنت في المركز رقم "
                f"{ranking.rank_position} "
                f"هذا الأسبوع"
            )
        )

    return "Weekly notifications sent"


# ==========================================
# WEEKLY REWARDS
# ==========================================

@shared_task
def weekly_rewards_task():

    current_week = (
        timezone.localdate().isocalendar().week
    )

    rankings = (
        WeeklyRanking.objects
        .filter(
            week_number=current_week
        )
        .order_by("rank_position")
    )

    # قيم المكافآت يمكن تعديلها لاحقًا
    reward_values = {
        1: 1000,
        2: 750,
        3: 500,
        4: 250,
        5: 100,
    }

    for ranking in rankings:

        amount = reward_values.get(
            ranking.rank_position,
            0
        )

        ranking.reward_amount = amount

        ranking.save(
            update_fields=[
                "reward_amount"
            ]
        )

        if amount > 0:

            Reward.objects.update_or_create(
                user=ranking.user,
                week_number=current_week,
                defaults={
                    "amount": amount,
                    "is_paid": False,
                }
            )

    return "Weekly rewards calculated"