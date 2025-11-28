"""
Сериализаторы для приложения courses.

Содержит сериализаторы для всех моделей курса:
- Категории курсов (CategorySerializer)
- Курсы (CourseSerializer, CourseDetailSerializer)
- Уроки (LessonSerializer, LessonDetailSerializer, LessonMaterialSerializer)
- Задания (AssignmentSerializer, AssignmentFileSerializer)
- Ответы на задания (SubmissionSerializer, SubmissionWithFilesSerializer, SubmissionFileSerializer)
- Оценки (GradeSerializer)
"""

from rest_framework import serializers
from .models import (
    Category, Course, CourseEnrollment, Lesson, LessonMaterial,
    Assignment, AssignmentFile, Submission, SubmissionFile, Grade
)
from users.serializers import BasicUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категорий курсов.

    Используется для просмотра списка категорий и их деталей.
    Категории используются для группировки курсов по темам.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для курсов (список).

    Используется для отображения списка курсов с основной информацией.
    Включает вычисляемые поля для удобства отображения.

    Дополнительные поля:
    - teacher_name: полное имя преподавателя
    - category_name: название категории
    - enrolled_count: количество записанных студентов
    - cover_image_url: URL обложки курса
    """
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    enrolled_count = serializers.ReadOnlyField()
    cover_image_url = serializers.ImageField(source='cover_image', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'teacher', 'teacher_name',
            'category', 'category_name', 'cover_image', 'cover_image_url',
            'status', 'difficulty', 'duration_weeks', 'max_students',
            'enrolled_count', 'is_featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['teacher', 'enrolled_count']


class CourseDetailSerializer(CourseSerializer):
    """
    Детальный сериализатор для курсов.

    Наследуется от CourseSerializer, добавляет дополнительные поля для детального просмотра.

    Дополнительные поля:
    - description: полное описание курса
    - lessons_count: количество опубликованных уроков
    - assignments_count: общее количество заданий во всех уроках
    - is_enrolled: записан ли текущий пользователь на курс
    - progress: процент прогресса текущего пользователя (если записан)
    """
    teacher = BasicUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    lessons_count = serializers.SerializerMethodField()
    assignments_count = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + [
            'description', 'lessons_count', 'assignments_count',
            'is_enrolled', 'progress'
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.filter(is_published=True).count()

    def get_assignments_count(self, obj):
        return sum(lesson.assignments.count() for lesson in obj.lessons.filter(is_published=True))

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(student=request.user, is_active=True).exists()
        return False

    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            enrollment = obj.enrollments.filter(student=request.user, is_active=True).first()
            return enrollment.progress if enrollment else 0
        return 0


class LessonMaterialSerializer(serializers.ModelSerializer):
    """
    Сериализатор для материалов урока.

    Материалы урока - это файлы (PDF, документы, видео, изображения),
    прикрепленные к уроку для дополнительного изучения.

    Дополнительные поля:
    - file_url: URL для скачивания файла
    """
    file_url = serializers.FileField(source='file', read_only=True)

    class Meta:
        model = LessonMaterial
        fields = [
            'id', 'title', 'file', 'file_url', 'file_type', 'file_size',
            'description', 'order', 'uploaded_at'
        ]


class LessonSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для уроков.

    Используется для списка уроков курса.

    Дополнительные поля:
    - materials_count: количество прикрепленных материалов
    """
    course = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Course.objects.all(),
        required=True
    )
    materials_count = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'title', 'slug', 'description', 'order', 'duration_minutes',
            'is_published', 'video_url', 'materials_count', 'created_at', 'updated_at'
        ]

    def get_materials_count(self, obj):
        return obj.materials.count()


class LessonDetailSerializer(LessonSerializer):
    """
    Детальный сериализатор для уроков.

    Наследуется от LessonSerializer, добавляет контент и материалы.

    Дополнительные поля:
    - content: полный текст урока
    - materials: список всех материалов урока
    - assignments_count: количество заданий в уроке
    - course: вложенный сериализатор курса
    """
    course = CourseSerializer(read_only=True)
    materials = LessonMaterialSerializer(many=True, read_only=True)
    assignments_count = serializers.SerializerMethodField()

    class Meta(LessonSerializer.Meta):
        fields = LessonSerializer.Meta.fields + [
            'content', 'materials', 'assignments_count'
        ]

    def get_assignments_count(self, obj):
        return obj.assignments.count()


class AssignmentFileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для файлов заданий.

    Файлы, прикрепленные к заданию преподавателем для дополнительной информации.

    Дополнительные поля:
    - file_url: URL для скачивания файла
    """
    file_url = serializers.FileField(source='file', read_only=True)

    class Meta:
        model = AssignmentFile
        fields = ['id', 'file', 'file_url', 'filename', 'file_size', 'uploaded_at']


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заданий.

    Задания - это работы, которые студенты должны выполнить и сдать.

    Дополнительные поля:
    - files: список прикрепленных файлов
    - submissions_count: количество отправленных решений
    - is_submitted: отправил ли текущий студент решение
    """
    lesson = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Lesson.objects.all(),
        required=True
    )
    files = AssignmentFileSerializer(many=True, read_only=True)
    submissions_count = serializers.SerializerMethodField()
    is_submitted = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = [
            'id', 'lesson', 'title', 'description', 'instructions', 'max_score',
            'due_date', 'is_required', 'allow_late_submission',
            'files', 'submissions_count', 'is_submitted',
            'created_at', 'updated_at'
        ]

    def get_submissions_count(self, obj):
        return obj.submissions.count()

    def get_is_submitted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.is_student:
            return obj.submissions.filter(student=request.user).exists()
        return False


class SubmissionFileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для файлов ответов студентов.

    Файлы, прикрепленные к решению задания студентом.

    Дополнительные поля:
    - file_url: URL для скачивания файла
    """
    file_url = serializers.FileField(source='file', read_only=True)

    class Meta:
        model = SubmissionFile
        fields = ['id', 'file', 'file_url', 'filename', 'file_size', 'uploaded_at']


class SubmissionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ответов на задания.

    Решения заданий, отправленные студентами.

    Дополнительные поля:
    - student_name: полное имя студента
    - assignment_title: название задания
    - files_count: количество прикрепленных файлов
    """
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    files_count = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'assignment_title', 'student', 'student_name',
            'content', 'status', 'submitted_at', 'updated_at', 'is_late', 'files_count'
        ]
        read_only_fields = ['student', 'status', 'submitted_at', 'updated_at', 'is_late']

    def get_files_count(self, obj):
        return obj.files.count()


class SubmissionWithFilesSerializer(SubmissionSerializer):
    """
    Сериализатор для ответов с файлами.

    Наследуется от SubmissionSerializer, добавляет список файлов.
    Используется для детального просмотра решения с прикрепленными файлами.

    Дополнительные поля:
    - files: список всех файлов решения
    """
    files = SubmissionFileSerializer(many=True, read_only=True)

    class Meta(SubmissionSerializer.Meta):
        fields = SubmissionSerializer.Meta.fields + ['files']


class GradeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для оценок.

    Оценки, выставленные преподавателями за выполненные задания.

    Дополнительные поля:
    - submission_content: текст решения
    - student_name: имя студента
    - assignment_title: название задания
    - graded_by_name: имя преподавателя, выставившего оценку
    """
    submission_content = serializers.CharField(source='submission.content', read_only=True)
    student_name = serializers.CharField(source='submission.student.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='submission.assignment.title', read_only=True)
    graded_by_name = serializers.CharField(source='graded_by.get_full_name', read_only=True)

    class Meta:
        model = Grade
        fields = [
            'id', 'submission', 'submission_content', 'student_name', 'assignment_title',
            'score', 'feedback', 'graded_by', 'graded_by_name',
            'graded_at', 'updated_at'
        ]
        read_only_fields = ['graded_by', 'graded_at', 'updated_at']
