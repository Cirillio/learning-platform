from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """
    Категория курса
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Слаг'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Иконка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Курс
    """
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'Архивирован'),
    )
    
    DIFFICULTY_CHOICES = (
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    short_description = models.CharField(
        max_length=500,
        verbose_name='Краткое описание'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_teaching',
        limit_choices_to={'role': 'teacher'},
        verbose_name='Преподаватель'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
        verbose_name='Категория'
    )
    cover_image = models.ImageField(
        upload_to='course_covers/',
        null=True,
        blank=True,
        verbose_name='Обложка курса'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус'
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner',
        verbose_name='Сложность'
    )
    duration_weeks = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Длительность (недели)'
    )
    max_students = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Максимум студентов'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Избранный'
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
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def enrolled_count(self):
        return self.enrollments.filter(is_active=True).count()


class CourseEnrollment(models.Model):
    """
    Запись студента на курс
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_enrollments',
        limit_choices_to={'role': 'student'},
        verbose_name='Студент'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Курс'
    )
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата записи'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата завершения'
    )
    progress = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Прогресс (%)'
    )
    
    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class Lesson(models.Model):
    """
    Урок в курсе
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    content = models.TextField(
        verbose_name='Содержание'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Длительность (мин)'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )
    video_url = models.URLField(
        blank=True,
        verbose_name='Ссылка на видео'
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
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['course', 'order']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class LessonMaterial(models.Model):
    """
    Материалы урока (файлы, документы)
    """
    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('doc', 'Document'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('other', 'Other'),
    )
    
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name='Урок'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    file = models.FileField(
        upload_to='lesson_materials/',
        verbose_name='Файл'
    )
    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPES,
        default='other',
        verbose_name='Тип файла'
    )
    file_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Размер файла (байты)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )
    
    class Meta:
        verbose_name = 'Материал урока'
        verbose_name_plural = 'Материалы уроков'
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class Assignment(models.Model):
    """
    Задание для студентов
    """
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Урок'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    instructions = models.TextField(
        verbose_name='Инструкции'
    )
    max_score = models.PositiveIntegerField(
        default=100,
        verbose_name='Максимальный балл'
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Срок сдачи'
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name='Обязательное'
    )
    allow_late_submission = models.BooleanField(
        default=False,
        verbose_name='Разрешить позднюю сдачу'
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
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['lesson', '-created_at']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class AssignmentFile(models.Model):
    """
    Файлы, прикрепленные к заданию
    """
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Задание'
    )
    file = models.FileField(
        upload_to='assignment_files/',
        verbose_name='Файл'
    )
    filename = models.CharField(
        max_length=255,
        verbose_name='Имя файла'
    )
    file_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Размер файла (байты)'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )
    
    class Meta:
        verbose_name = 'Файл задания'
        verbose_name_plural = 'Файлы заданий'
    
    def __str__(self):
        return f"{self.assignment.title} - {self.filename}"


class Submission(models.Model):
    """
    Ответ студента на задание
    """
    STATUS_CHOICES = (
        ('pending', 'Ожидает проверки'),
        ('graded', 'Оценено'),
        ('returned', 'Возвращено на доработку'),
    )
    
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Задание'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions',
        limit_choices_to={'role': 'student'},
        verbose_name='Студент'
    )
    content = models.TextField(
        verbose_name='Ответ'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отправки'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    is_late = models.BooleanField(
        default=False,
        verbose_name='Просрочено'
    )
    
    class Meta:
        verbose_name = 'Ответ на задание'
        verbose_name_plural = 'Ответы на задания'
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"


class SubmissionFile(models.Model):
    """
    Файлы, прикрепленные к ответу студента
    """
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Ответ'
    )
    file = models.FileField(
        upload_to='submission_files/',
        verbose_name='Файл'
    )
    filename = models.CharField(
        max_length=255,
        verbose_name='Имя файла'
    )
    file_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Размер файла (байты)'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )
    
    class Meta:
        verbose_name = 'Файл ответа'
        verbose_name_plural = 'Файлы ответов'
    
    def __str__(self):
        return f"{self.submission.student.username} - {self.filename}"


class Grade(models.Model):
    """
    Оценка за задание
    """
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='grade',
        verbose_name='Ответ'
    )
    score = models.PositiveIntegerField(
        verbose_name='Баллы'
    )
    feedback = models.TextField(
        blank=True,
        verbose_name='Обратная связь'
    )
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='grades_given',
        limit_choices_to={'role': 'teacher'},
        verbose_name='Оценил'
    )
    graded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оценки'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ['-graded_at']
    
    def __str__(self):
        return f"{self.submission.student.username} - {self.submission.assignment.title} - {self.score}"

