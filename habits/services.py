from django.utils import timezone
from .models import Habit
from django.db.models import Q

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_habits_to_notify():
    current_time = timezone.now()
    logger.info(f"Текущее время: {current_time.strftime('%H:%M')}")

    habits = Habit.objects.filter(
        Q(time__hour=current_time.hour, time__minute=current_time.minute)
    )

    logger.info(f"Найдено привычек для уведомления: {habits.count()}")
    return habits
