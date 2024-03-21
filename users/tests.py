from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersAPITests(APITestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password2')

        # Авторизация пользователя
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        url = reverse('users:user-list')  # Предположим, что такой URL существует для регистрации
        user_data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_obtain_token(self):
        url = reverse('users:token_obtain_pair')
        credentials = {
            'email': 'user@example.com',
            'password': 'password',
        }
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_registration_with_invalid_email(self):
        url = reverse('users:user-list')
        user_data = {
            'email': 'not_an_email',
            'password': 'password123',
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('email' in response.data)

    def test_user_obtain_token_with_wrong_password(self):
        url = reverse('users:token_obtain_pair')
        credentials = {
            'email': 'user@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(url, credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
