from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'email_sent', 'created_at']
    list_filter = ['notification_type', 'is_read', 'email_sent', 'created_at']
    search_fields = ['title', 'message', 'recipient__username']
    readonly_fields = ['created_at', 'read_at', 'email_sent_at']
    
    fieldsets = (
        ('Recipient', {'fields': ('recipient', 'notification_type')}),
        ('Content', {'fields': ('title', 'message')}),
        ('Related Object', {'fields': ('content_type', 'object_id')}),
        ('Status', {'fields': ('is_read', 'read_at')}),
        ('Email', {'fields': ('email_sent', 'email_sent_at')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        for notification in queryset:
            notification.mark_as_read()
        self.message_user(request, f'{queryset.count()} уведомлений помечено как прочитанные')
    mark_as_read.short_description = 'Пометить как прочитанное'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{queryset.count()} уведомлений помечено как непрочитанные')
    mark_as_unread.short_description = 'Пометить как непрочитанное'
