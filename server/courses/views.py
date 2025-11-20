from rest_framework import viewsets, status, filters, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Avg
from django.utils import timezone
from rest_framework.views import APIView
from django.urls import reverse

from courses.pagination import CoursePagination # Added this import

from .models import (
    Category, Course, CourseEnrollment, Lesson, LessonMaterial,
    Assignment, AssignmentFile, Submission, SubmissionFile, Grade
)
from .serializers import (
    CategorySerializer, CourseSerializer, CourseDetailSerializer,
    LessonSerializer, LessonDetailSerializer, LessonMaterialSerializer,
    AssignmentSerializer, AssignmentFileSerializer,
    SubmissionSerializer, SubmissionWithFilesSerializer, SubmissionFileSerializer,
    GradeSerializer
)
from .permissions import IsTeacher, IsStudent, IsCourseOwner, IsTeacherOrReadOnly
from .tasks import send_grade_notification, send_new_assignment_notification


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для категорий курсов.
    Только для чтения (list, retrieve).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.
    
    - list: список всех опубликованных курсов (студенты) или всех курсов (преподаватели)
    - retrieve: детали курса
    - create: создание курса (только преподаватели)
    - update/partial_update: обновление курса (только владелец курса)
    - destroy: удаление курса (только владелец курса)
    
    Дополнительные actions:
    - enroll: запись студента на курс
    - unenroll: отмена записи на курс
    - my_courses: список курсов текущего пользователя
    - students: список студентов курса (только для преподавателя курса)
    """
    queryset = Course.objects.all()
    pagination_class = CoursePagination  # <-- добавь это
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['created_at', 'title', 'difficulty']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по категории
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Фильтрация по сложности
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Фильтрация по статусу
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Студенты видят только опубликованные курсы (кроме тех, на которые записаны)
        if self.request.user.is_authenticated and self.request.user.role == 'student':
            enrolled_courses = self.request.user.course_enrollments.filter(
                is_active=True
            ).values_list('course_id', flat=True)
            queryset = queryset.filter(
                Q(status='published') | Q(id__in=enrolled_courses)
            )
        
        return queryset.select_related('teacher', 'category').annotate(
            enrollments_count=Count('enrollments', filter=Q(enrollments__is_active=True))
        )
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsTeacher()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCourseOwner()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStudent])
    def enroll(self, request, slug=None):
        """
        Записать студента на курс.
        POST /api/courses/{slug}/enroll/
        """
        course = self.get_object()
        
        # Проверка максимального количества студентов
        if course.max_students:
            current_count = course.enrollments.filter(is_active=True).count()
            if current_count >= course.max_students:
                return Response(
                    {'detail': 'Достигнуто максимальное количество студентов.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Создание или обновление записи
        enrollment, created = CourseEnrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'is_active': True}
        )
        
        if not created and enrollment.is_active:
            return Response(
                {'detail': 'Вы уже записаны на этот курс.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not created:
            enrollment.is_active = True
            enrollment.save()
        
        # Обновляем количество студентов
        current_enrollments = course.enrollments.filter(is_active=True).count()
        
        return Response(
            {
                'detail': 'Вы успешно записались на курс.',
                'enrollment': {
                    'id': enrollment.id,
                    'course_id': course.id,
                    'course_slug': course.slug,
                    'enrolled_at': enrollment.enrolled_at,
                    'is_active': enrollment.is_active,
                    'progress': enrollment.progress,
                },
                'course': {
                    'enrollments_count': current_enrollments,
                    'spots_left': course.max_students - current_enrollments if course.max_students else None,
                }
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStudent])
    def unenroll(self, request, slug=None):
        """
        Отменить запись на курс.
        POST /api/courses/{slug}/unenroll/
        """
        course = self.get_object()
        
        try:
            enrollment = CourseEnrollment.objects.get(
                student=request.user,
                course=course,
                is_active=True
            )
            enrollment.is_active = False
            enrollment.save()
            
            # Обновляем количество студентов
            current_enrollments = course.enrollments.filter(is_active=True).count()
            
            return Response(
                {
                    'detail': 'Вы отменили запись на курс.',
                    'enrollment': {
                        'id': enrollment.id,
                        'course_id': course.id,
                        'course_slug': course.slug,
                        'is_active': enrollment.is_active,
                        'unenrolled_at': timezone.now(),
                    },
                    'course': {
                        'enrollments_count': current_enrollments,
                        'spots_left': course.max_students - current_enrollments if course.max_students else None,
                    }
                },
                status=status.HTTP_200_OK
            )
        except CourseEnrollment.DoesNotExist:
            return Response(
                {'detail': 'Вы не записаны на этот курс.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_courses(self, request):
        """
        Получить список курсов текущего пользователя.
        - Для преподавателя: курсы, которые он ведет
        - Для студента: курсы, на которые он записан
        GET /api/courses/my_courses/
        """
        if request.user.role == 'teacher':
            courses = Course.objects.filter(teacher=request.user)
        else:
            enrollments = CourseEnrollment.objects.filter(
                student=request.user,
                is_active=True
            ).values_list('course_id', flat=True)
            courses = Course.objects.filter(id__in=enrollments)
        
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsCourseOwner])
    def students(self, request, slug=None):
        """
        Получить список студентов курса.
        Доступно только преподавателю курса.
        GET /api/courses/{slug}/students/
        """
        course = self.get_object()
        enrollments = CourseEnrollment.objects.filter(
            course=course,
            is_active=True
        ).select_related('student')
        
        students_data = [{
            'id': enrollment.student.id,
            'username': enrollment.student.username,
            'email': enrollment.student.email,
            'first_name': enrollment.student.first_name,
            'last_name': enrollment.student.last_name,
            'enrolled_at': enrollment.enrolled_at,
            'progress': enrollment.progress,
        } for enrollment in enrollments]
        
        return Response(students_data)


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления уроками.
    
    - list: список уроков курса
    - retrieve: детали урока
    - create: создание урока (только преподаватель курса)
    - update/partial_update: обновление урока (только преподаватель курса)
    - destroy: удаление урока (только преподаватель курса)
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LessonDetailSerializer
        return LessonSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по курсу
        course_slug = self.request.query_params.get('course', None)
        if course_slug:
            queryset = queryset.filter(course__slug=course_slug)
        
        # Студенты видят только опубликованные уроки
        if self.request.user.is_authenticated and self.request.user.role == 'student':
            queryset = queryset.filter(is_published=True)
        
        return queryset.select_related('course').prefetch_related('materials', 'assignments')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTeacher()]
        return super().get_permissions()


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заданиями.
    
    - list: список заданий
    - retrieve: детали задания
    - create: создание задания (только преподаватель)
    - update/partial_update: обновление задания (только преподаватель)
    - destroy: удаление задания (только преподаватель)
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по уроку
        lesson_id = self.request.query_params.get('lesson', None)
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        
        # Фильтрация по курсу
        course_slug = self.request.query_params.get('course', None)
        if course_slug:
            queryset = queryset.filter(lesson__course__slug=course_slug)
        
        return queryset.select_related('lesson', 'lesson__course').prefetch_related('files')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTeacher()]
        return super().get_permissions()

    def perform_create(self, serializer):
        assignment = serializer.save()
        # Отправляем уведомление о новом задании
        send_new_assignment_notification.delay(assignment.id)


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления ответами на задания.
    
    - list: список ответов (преподаватель видит все, студент - только свои)
    - retrieve: детали ответа
    - create: создание ответа (только студент)
    - update/partial_update: обновление ответа (только автор)
    - destroy: удаление ответа (только автор)
    """
    queryset = Submission.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return SubmissionWithFilesSerializer
        return SubmissionSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по заданию
        assignment_id = self.request.query_params.get('assignment', None)
        if assignment_id:
            queryset = queryset.filter(assignment_id=assignment_id)
        
        # Студенты видят только свои ответы
        if self.request.user.role == 'student':
            queryset = queryset.filter(student=self.request.user)
        
        return queryset.select_related(
            'assignment', 'student', 'assignment__lesson', 'assignment__lesson__course'
        ).prefetch_related('files', 'grade')
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsStudent()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        assignment = serializer.validated_data['assignment']
        
        # Проверка срока сдачи
        is_late = False
        if assignment.due_date and timezone.now() > assignment.due_date:
            if not assignment.allow_late_submission:
                raise serializers.ValidationError(
                    'Срок сдачи задания истек.'
                )
            is_late = True
        
        serializer.save(student=self.request.user, is_late=is_late)


class GradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления оценками.
    
    - list: список оценок
    - retrieve: детали оценки
    - create: выставление оценки (только преподаватель)
    - update/partial_update: обновление оценки (только преподаватель)
    - destroy: удаление оценки (только преподаватель)
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по ответу
        submission_id = self.request.query_params.get('submission', None)
        if submission_id:
            queryset = queryset.filter(submission_id=submission_id)
        
        # Студенты видят только свои оценки
        if self.request.user.role == 'student':
            queryset = queryset.filter(submission__student=self.request.user)
        
        return queryset.select_related(
            'submission', 'submission__student', 'submission__assignment', 'graded_by'
        )
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTeacher()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # Обновляем статус ответа на "оценено"
        submission = serializer.validated_data['submission']
        submission.status = 'graded'
        submission.save()
        
        grade = serializer.save(graded_by=self.request.user)
        # Отправляем уведомление студенту о новой оценке
        send_grade_notification.delay(grade.id)

class CourseFilterOptionsView(APIView):
    """
    Предоставляет возможные значения для фильтров курсов.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        difficulty_choices = [{'value': choice[0], 'label': choice[1]} for choice in Course.DIFFICULTY_CHOICES]
        status_choices = [{'value': choice[0], 'label': choice[1]} for choice in Course.STATUS_CHOICES]
        
        ordering_options = [
            {'value': 'created_at', 'label': 'По дате создания (сначала старые)'},
            {'value': '-created_at', 'label': 'По дате создания (сначала новые)'},
            {'value': 'title', 'label': 'По названию (А-Я)'},
            {'value': '-title', 'label': 'По названию (Я-А)'},
            {'value': 'difficulty', 'label': 'По сложности (от простого к сложному)'},
            {'value': '-difficulty', 'label': 'По сложности (от сложного к простому)'},
        ]

        categories = Category.objects.all()
        category_choices = [{'value': cat.slug, 'label': cat.name} for cat in categories]

        return Response({
            'filters': [
                {
                    'value': 'difficulty',
                    'label': 'Сложность',
                    'values': difficulty_choices
                },
                {
                    'value': 'status',
                    'label': 'Статус',
                    'values': status_choices
                },
                {
                    'value': 'ordering',
                    'label': 'Сортировка',
                    'values': ordering_options
                },
                {
                    'value': 'category',
                    'label': 'Категория',
                    'values': category_choices
                }
            ],
        })


