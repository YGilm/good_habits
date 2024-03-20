from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Фотография', **NULLABLE)
    chat_id = models.CharField(max_length=30, verbose_name='telegram id', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='Статус пользователя')
    is_staff = models.BooleanField(default=False, verbose_name='Статус сотрудника')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'Пользователь {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
