from celery import shared_task
from django.conf import settings
import logging
import requests

from habits.services import get_habits_to_notify

# Настройка логгера
logger = logging.getLogger(__name__)


@shared_task
def send_telegram_notification(chat_id, message):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logger.info(f"Сообщение отправлено: {response.json()}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")


@shared_task
def notify_users_about_habits():
    habits = get_habits_to_notify()
    if not habits:
        logger.info("Нет привычек для уведомления.")
        return
    for habit in habits:
        user = habit.user
        chat_id = user.chat_id
        if not chat_id:
            logger.error(f"У пользователя {user.email} нет chat_id.")
            continue
        message = f"Напоминание: {habit.action} {habit.location} в {habit.time.strftime('%H:%M')}"
        logger.info(f"Отправка сообщения '{message}' в чат {chat_id} для пользователя {user.email}.")
        send_telegram_notification.delay(chat_id, message)
