from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default='student'
    )

    # Поля профиля
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)

    # Для преподавателей
    specialization = serializers.CharField(max_length=200, required=False, allow_blank=True)
    experience_years = serializers.IntegerField(required=False, allow_null=True, min_value=0)

    # Для студентов
    student_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
    enrollment_year = serializers.IntegerField(required=False, allow_null=True, min_value=1900)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 'role',
            'first_name', 'last_name',
            'bio', 'phone', 'birth_date', 'address', 'city', 'country',
            'specialization', 'experience_years', 'student_id', 'enrollment_year'
        ]
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают."})

        # Валидация роли-специфичных полей
        role = attrs.get('role')
        if role == 'teacher':
            if not attrs.get('specialization'):
                raise serializers.ValidationError({"specialization": "Специализация обязательна для преподавателей."})
        elif role == 'student':
            if not attrs.get('student_id'):
                raise serializers.ValidationError({"student_id": "Студенческий билет обязателен для студентов."})

        return attrs

    def create(self, validated_data):
        # Извлекаем поля профиля
        profile_data = {
            'bio': validated_data.pop('bio', ''),
            'phone': validated_data.pop('phone', ''),
            'birth_date': validated_data.pop('birth_date', None),
            'address': validated_data.pop('address', ''),
            'city': validated_data.pop('city', ''),
            'country': validated_data.pop('country', ''),
            'specialization': validated_data.pop('specialization', ''),
            'experience_years': validated_data.pop('experience_years', None),
            'student_id': validated_data.pop('student_id', ''),
            'enrollment_year': validated_data.pop('enrollment_year', None),
        }

        # Удаляем password_confirm
        validated_data.pop('password_confirm')

        # Создаем пользователя
        user = User.objects.create_user(**validated_data)

        # Создаем профиль
        UserProfile.objects.create(user=user, **profile_data)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя
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
        read_only_fields = ['user', 'created_at', 'updated_at']

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