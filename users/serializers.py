from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'city', 'avatar', 'chat_id')
        extra_kwargs = {'password': {'write_only': True}}
        permission_classes = [IsAuthenticated]

    def create(self, validated_data):
        # Хеширование пароля перед сохранением
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
