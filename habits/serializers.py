from rest_framework import serializers
from .models import Habit
from .validators import validate_max_duration, validate_exclusive_fields, validate_pleasant_habit, validate_periodicity


# Предполагается, что функции валидации были импортированы или определены здесь же.

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, attrs):
        # Проверяем длительность привычки
        if 'duration' in attrs:
            validate_max_duration(attrs['duration'])

        # Проверяем, что не установлены одновременно связанная привычка и вознаграждение
        validate_exclusive_fields(attrs)

        # Проверяем, что связанная привычка приятная, и приятная привычка не имеет вознаграждения или связанной привычки
        validate_pleasant_habit(attrs)

        # Проверяем периодичность выполнения привычки
        if 'frequency' in attrs:
            validate_periodicity(attrs['frequency'])

        return attrs
