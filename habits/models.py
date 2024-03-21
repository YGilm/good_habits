from django.db import models
from django.conf import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits',
                             verbose_name='Пользователь')
    location = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.TextField(verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='related_habits', verbose_name='Связанная привычка')
    frequency = models.IntegerField(default=1, verbose_name='Периодичность (дни)')
    reward = models.TextField(blank=True, verbose_name='Вознаграждение')
    duration = models.IntegerField(verbose_name='Время на выполнение (минуты)')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)

    def __str__(self):
        return f'{self.action} в {self.location} в {self.time}'
