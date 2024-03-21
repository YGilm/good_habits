from django.core.exceptions import ValidationError


def validate_max_duration(value, max_duration=2):
    if value is not None and value > max_duration:
        raise ValidationError(f'Время на выполнение не должно превышать {max_duration} минут.')


def validate_exclusive_fields(attrs):
    related_habit = attrs.get('related_habit')
    reward = attrs.get('reward')
    if related_habit and reward:
        raise ValidationError("Не может быть одновременно установлены связанная привычка и вознаграждение.")


def validate_pleasant_habit(attrs):
    related_habit = attrs.get('related_habit')
    is_pleasant = attrs.get('is_pleasant')
    reward = attrs.get('reward')
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной.")
    if is_pleasant and (related_habit or reward):
        raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


def validate_periodicity(frequency, max_period=7):
    if frequency is not None and (frequency < 1 or frequency > max_period):
        raise ValidationError(f"Периодичность выполнения привычки должна быть от 1 до {max_period} дней.")
