"""
Сериализаторы для приложения users.

Содержит сериализаторы для:
- Регистрации пользователей (UserRegistrationSerializer)
- Управления профилями пользователей (UserProfileSerializer)
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для пользователя.
    
    Используется для отображения информации о пользователе
    в списках и ссылках.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class BasicUserSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для пользователя, используемый для вложенных объектов.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    Создает только пользователя, профиль создается через сигнал.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    role = serializers.HiddenField(default='student')

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 'role',
            'first_name', 'last_name'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.

    Позволяет просматривать и редактировать профиль пользователя.
    Включает поля из модели User (только для чтения) и UserProfile.

    Особенности:
    - username, email, role, date_joined: только для чтения
    - first_name, last_name: можно редактировать
    - avatar: изображение профиля
    - Роле-специфичные поля (specialization, experience_years для преподавателей;
      student_id, enrollment_year для студентов)
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    role = serializers.CharField(source='user.role', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user', 'username', 'email', 'first_name', 'last_name', 'role', 'date_joined',
            'avatar', 'bio', 'phone', 'birth_date', 'address', 'city', 'country',
            'specialization', 'experience_years', 'student_id', 'enrollment_year',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'student_id', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Обновляем поля пользователя
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Обновляем поля профиля
        return super().update(instance, validated_data)