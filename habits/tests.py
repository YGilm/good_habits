from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitAPITests(APITestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password2')

        # Авторизация пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем привычку
        self.habit = Habit.objects.create(
            user=self.user,
            location='Дома',
            time='07:00:00',
            action='Утренняя пробежка',
            is_pleasant=True,
            frequency=1,
            reward='Здоровье',
            duration=30,
            is_public=True
        )

    def test_view_habit_list(self):
        url = reverse('habits:habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Habit.objects.count())

    def test_user_habits_list(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse('habits:habit-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка, что в ответе нет привычек первого пользователя
        self.assertNotIn(self.habit.action, str(response.data))

    def test_view_habit_detail(self):
        url = reverse('habits:habit-detail', args=[self.habit.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], self.habit.action)

    def test_delete_habit(self):
        # Удаляем привычку
        response = self.client.delete(reverse('habits:habit-detail', args=[self.habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit.pk).exists())

    def test_update_habit_unauthorized(self):
        # Попытка обновить привычку другого пользователя
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(reverse('habits:habit-detail', args=[self.habit.pk]),
                                     {'action': 'Вечерняя пробежка'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_frequency_validation_on_update(self):
        # Обновляем привычку с невалидной периодичностью
        response = self.client.patch(reverse('habits:habit-detail', args=[self.habit.pk]), {'frequency': 8},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_msg = response.data['non_field_errors'][0]
        self.assertEqual("Периодичность выполнения привычки должна быть от 1 до 7 дней.", error_msg)

    def test_is_pleasant_validation_on_update(self):
        # Попытка установить невалидное значение для is_pleasant при наличии связанной привычки
        related_habit = Habit.objects.create(
            user=self.user,
            location='Дома',
            time='20:00:00',
            action='Чтение книги',
            is_pleasant=False,
            frequency=1,
            reward='',
            duration=30,
            is_public=True
        )
        response = self.client.patch(reverse('habits:habit-detail', args=[self.habit.pk]),
                                     {'related_habit': related_habit.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Используйте response.data для получения сообщений об ошибках
        error_msg = response.data['non_field_errors'][0]
        self.assertEqual("Связанная привычка должна быть приятной.", error_msg)

    def test_habit_list_pagination(self):
        # Создаем дополнительные привычки
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                location='Место выполнения ' + str(i),
                time='07:00:00',
                action='Привычка ' + str(i),
                is_pleasant=i % 2 == 0,  # Для разнообразия: половина привычек приятные, половина нет
                frequency=1,
                reward='Награда ' + str(i) if i % 2 == 0 else '',
                duration=30,
                is_public=True
            )

        response = self.client.get(reverse('habits:habit-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка, что в ответе ровно 5 объектов, как определено в настройках пагинатора
        self.assertEqual(len(response.data['results']), 5)

        # Дополнительно можете проверить, что в ответе есть ссылки на следующую и предыдущую страницы
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_update_habit_by_another_user(self):
        url = reverse('habits:habit-detail', args=[self.habit.pk])
        self.client.force_authenticate(user=self.user2)  # Авторизуем второго пользователя
        response = self.client.patch(url, {'action': 'Вечерняя йога'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
