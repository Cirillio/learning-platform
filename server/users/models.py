from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя с ролями
    """
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='Роль'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_student(self):
        return self.role == 'student'


class UserProfile(models.Model):
    """
    Профиль пользователя с дополнительной информацией
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Адрес'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Город'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Страна'
    )
    
    # Для преподавателей
    specialization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Специализация'
    )
    experience_years = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Опыт работы (лет)'
    )
    
    # Для студентов
    student_id = models.CharField(
        max_length=50,
        blank=True,
        unique=True,
        null=True,
        verbose_name='Студенческий билет'
    )
    enrollment_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Год поступления'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"Профиль {self.user.username}"
