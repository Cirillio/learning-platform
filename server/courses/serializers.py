from rest_framework import serializers
from .models import (
    Category, Course, CourseEnrollment, Lesson, LessonMaterial,
    Assignment, AssignmentFile, Submission, SubmissionFile, Grade, Comment
)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категорий курсов
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для курсов (список)
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
    Детальный сериализатор для курсов
    """
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
    Сериализатор для материалов урока
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
    Базовый сериализатор для уроков
    """
    materials_count = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'slug', 'description', 'order', 'duration_minutes',
            'is_published', 'video_url', 'materials_count', 'created_at', 'updated_at'
        ]

    def get_materials_count(self, obj):
        return obj.materials.count()


class LessonDetailSerializer(LessonSerializer):
    """
    Детальный сериализатор для уроков
    """
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
    Сериализатор для файлов заданий
    """
    file_url = serializers.FileField(source='file', read_only=True)

    class Meta:
        model = AssignmentFile
        fields = ['id', 'file', 'file_url', 'filename', 'file_size', 'uploaded_at']


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заданий
    """
    files = AssignmentFileSerializer(many=True, read_only=True)
    submissions_count = serializers.SerializerMethodField()
    is_submitted = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'instructions', 'max_score',
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
    Сериализатор для файлов ответов
    """
    file_url = serializers.FileField(source='file', read_only=True)

    class Meta:
        model = SubmissionFile
        fields = ['id', 'file', 'file_url', 'filename', 'file_size', 'uploaded_at']


class SubmissionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ответов на задания
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
    Сериализатор для ответов с файлами
    """
    files = SubmissionFileSerializer(many=True, read_only=True)

    class Meta(SubmissionSerializer.Meta):
        fields = SubmissionSerializer.Meta.fields + ['files']


class GradeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для оценок
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


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев
    """
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_avatar = serializers.ImageField(source='author.profile.avatar', read_only=True)
    replies_count = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'content_type', 'object_id', 'author', 'author_name', 'author_avatar',
            'text', 'parent', 'replies_count', 'is_author',
            'created_at', 'updated_at', 'is_edited'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at', 'is_edited']

    def get_replies_count(self, obj):
        return obj.replies.count()

    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.author