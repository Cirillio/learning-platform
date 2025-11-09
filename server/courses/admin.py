from django.contrib import admin
from .models import (
    Category, Course, CourseEnrollment, Lesson, LessonMaterial,
    Assignment, AssignmentFile, Submission, SubmissionFile, Grade
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['title', 'order', 'is_published', 'duration_minutes']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'category', 'status', 'difficulty', 'is_featured', 'created_at']
    list_filter = ['status', 'difficulty', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'description', 'teacher__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LessonInline]
    
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'slug', 'teacher', 'category')}),
        ('Description', {'fields': ('short_description', 'description')}),
        ('Settings', {'fields': ('status', 'difficulty', 'duration_weeks', 'max_students', 'is_featured')}),
        ('Media', {'fields': ('cover_image',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'is_active', 'progress', 'completed_at']
    list_filter = ['is_active', 'enrolled_at', 'completed_at']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['enrolled_at']


class LessonMaterialInline(admin.TabularInline):
    model = LessonMaterial
    extra = 0
    fields = ['title', 'file_type', 'file', 'order']


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0
    fields = ['title', 'max_score', 'due_date', 'is_required']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_published', 'duration_minutes', 'created_at']
    list_filter = ['is_published', 'created_at', 'course']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LessonMaterialInline, AssignmentInline]
    
    fieldsets = (
        ('Basic Info', {'fields': ('course', 'title', 'slug', 'order')}),
        ('Content', {'fields': ('description', 'content', 'video_url')}),
        ('Settings', {'fields': ('is_published', 'duration_minutes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(LessonMaterial)
class LessonMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'file_type', 'file_size', 'order', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['title', 'description', 'lesson__title']
    readonly_fields = ['uploaded_at']


class AssignmentFileInline(admin.TabularInline):
    model = AssignmentFile
    extra = 0


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'max_score', 'due_date', 'is_required', 'allow_late_submission']
    list_filter = ['is_required', 'allow_late_submission', 'created_at', 'due_date']
    search_fields = ['title', 'description', 'lesson__title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AssignmentFileInline]


@admin.register(AssignmentFile)
class AssignmentFileAdmin(admin.ModelAdmin):
    list_display = ['filename', 'assignment', 'file_size', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['filename', 'assignment__title']
    readonly_fields = ['uploaded_at']


class SubmissionFileInline(admin.TabularInline):
    model = SubmissionFile
    extra = 0


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'status', 'is_late', 'submitted_at']
    list_filter = ['status', 'is_late', 'submitted_at']
    search_fields = ['student__username', 'assignment__title', 'content']
    readonly_fields = ['submitted_at', 'updated_at']
    inlines = [SubmissionFileInline]


@admin.register(SubmissionFile)
class SubmissionFileAdmin(admin.ModelAdmin):
    list_display = ['filename', 'submission', 'file_size', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['filename', 'submission__student__username']
    readonly_fields = ['uploaded_at']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['submission', 'score', 'graded_by', 'graded_at']
    list_filter = ['graded_at', 'graded_by']
    search_fields = ['submission__student__username', 'submission__assignment__title', 'feedback']
    readonly_fields = ['graded_at', 'updated_at']
