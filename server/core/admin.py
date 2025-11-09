from django.contrib import admin
from .models import Comment, Feedback, ActivityLog


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_type', 'object_id', 'text_preview', 'is_edited', 'created_at']
    list_filter = ['is_edited', 'created_at', 'content_type']
    search_fields = ['text', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'feedback_type', 'status', 'priority', 'created_at']
    list_filter = ['feedback_type', 'status', 'priority', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
    
    fieldsets = (
        ('Basic Info', {'fields': ('user', 'feedback_type', 'title', 'description')}),
        ('Status', {'fields': ('status', 'priority', 'screenshot')}),
        ('Response', {'fields': ('admin_response',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'resolved_at')}),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'description', 'ip_address']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Info', {'fields': ('user', 'action', 'description')}),
        ('Technical Info', {'fields': ('ip_address', 'user_agent')}),
        ('Related Object', {'fields': ('content_type', 'object_id')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
