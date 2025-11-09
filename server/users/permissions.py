"""
Permissions для приложения users.

Содержит permission классы для проверки ролей пользователей:
- IsTeacher: проверка, что пользователь является преподавателем
- IsStudent: проверка, что пользователь является студентом
"""

from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """
    Permission для проверки, что пользователь является преподавателем.

    Используется для эндпоинтов, доступных только преподавателям:
    - Создание и управление курсами
    - Выставление оценок
    - Управление заданиями

    Проверяет поле user.role == 'teacher'
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )


class IsStudent(BasePermission):
    """
    Permission для проверки, что пользователь является студентом.

    Используется для эндпоинтов, доступных только студентам:
    - Отправка решений на задания
    - Запись на курсы
    - Просмотр оценок

    Проверяет поле user.role == 'student'
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'student'
        )