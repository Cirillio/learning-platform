"""
Permissions для приложения courses.

Содержит permission классы для контроля доступа к объектам курсов:
- IsOwner: проверка, что пользователь является автором объекта
- IsCourseOwner: проверка, что пользователь является преподавателем курса
- IsTeacherOrReadOnly: преподаватели могут изменять, остальные только читать
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Permission для проверки, что пользователь является владельцем объекта.

    Определяет владельца в зависимости от типа объекта:
    - Course: obj.teacher
    - Lesson/Assignment/Grade: obj.course.teacher
    - Comment: obj.author
    - Submission: obj.student

    Используется для персональных объектов, где только владелец может изменять.
    """

    def has_object_permission(self, request, view, obj):
        # Определяем владельца в зависимости от типа объекта
        if hasattr(obj, 'teacher'):
            # Course
            owner = obj.teacher
        elif hasattr(obj, 'course') and hasattr(obj.course, 'teacher'):
            # Lesson, Assignment, etc.
            owner = obj.course.teacher
        elif hasattr(obj, 'author'):
            # Comment
            owner = obj.author
        elif hasattr(obj, 'student'):
            # Submission
            owner = obj.student
        else:
            return False

        return owner == request.user


class IsCourseOwner(BasePermission):
    """
    Permission для проверки, что пользователь является преподавателем курса.

    Используется для объектов, связанных с курсом:
    - Уроки, задания, оценки - только преподаватель курса может управлять
    - Студенты могут только просматривать

    Для list views: преподаватели могут создавать, остальные - только читать.
    Для object views: только преподаватель курса может изменять объект.
    """

    def has_permission(self, request, view):
        # Для list view проверяем, что пользователь - преподаватель
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )

    def has_object_permission(self, request, view, obj):
        # Определяем курс из объекта
        if hasattr(obj, 'course'):
            course = obj.course
        elif hasattr(obj, 'lesson') and hasattr(obj.lesson, 'course'):
            course = obj.lesson.course
        elif hasattr(obj, 'assignment') and hasattr(obj.assignment, 'lesson') and hasattr(obj.assignment.lesson, 'course'):
            course = obj.assignment.lesson.course
        else:
            return False

        return course.teacher == request.user


class IsTeacherOrReadOnly(BasePermission):
    """
    Permission: преподаватели могут выполнять любые действия,
    остальные пользователи только чтение.

    Используется для общих ресурсов:
    - Категории курсов
    - Публичные курсы
    - Общие материалы

    SAFE_METHODS (GET, HEAD, OPTIONS): доступны всем аутентифицированным пользователям
    Остальные методы (POST, PUT, DELETE): только преподавателям
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return (
                request.user and
                request.user.is_authenticated
            )
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Для изменения объектов проверяем, что пользователь - преподаватель
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )