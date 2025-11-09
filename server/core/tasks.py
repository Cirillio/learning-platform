"""
Celery tasks для core приложения.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import Comment
from notifications.models import Notification


@shared_task
def send_comment_notification(comment_id):
    """
    Отправить уведомление о новом комментарии.
    
    - Если это ответ на комментарий, уведомляем автора родительского комментария
    - Если это комментарий к уроку/заданию, уведомляем преподавателя
    """
    try:
        comment = Comment.objects.select_related(
            'author',
            'parent',
            'content_type'
        ).get(id=comment_id)
        
        recipients = []
        
        # Если это ответ на комментарий
        if comment.parent:
            parent_author = comment.parent.author
            if parent_author != comment.author:  # Не уведомляем самого себя
                recipients.append(parent_author)
                
                # Создаем уведомление
                Notification.objects.create(
                    recipient=parent_author,
                    notification_type='new_comment',
                    title='Новый ответ на ваш комментарий',
                    message=f'{comment.author.get_full_name() or comment.author.username} ответил на ваш комментарий: {comment.text[:100]}',
                    content_object=comment
                )
                
                # Отправляем email
                if parent_author.email:
                    send_mail(
                        subject='Новый ответ на ваш комментарий',
                        message=f'''
                        Здравствуйте, {parent_author.get_full_name() or parent_author.username}!
                        
                        {comment.author.get_full_name() or comment.author.username} ответил на ваш комментарий:
                        
                        "{comment.text}"
                        
                        Ваш комментарий:
                        "{comment.parent.text}"
                        ''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[parent_author.email],
                        fail_silently=True,
                    )
        
        # Если это комментарий к уроку, уведомляем преподавателя
        else:
            # Пытаемся получить связанный объект
            from courses.models import Lesson
            
            if comment.content_type.model == 'lesson':
                try:
                    lesson = Lesson.objects.select_related(
                        'course__teacher'
                    ).get(id=comment.object_id)
                    
                    teacher = lesson.course.teacher
                    
                    if teacher != comment.author:  # Не уведомляем самого себя
                        # Создаем уведомление
                        Notification.objects.create(
                            recipient=teacher,
                            notification_type='new_comment',
                            title=f'Новый комментарий к уроку: {lesson.title}',
                            message=f'{comment.author.get_full_name() or comment.author.username} оставил комментарий: {comment.text[:100]}',
                            content_object=comment
                        )
                        
                        # Отправляем email
                        if teacher.email:
                            send_mail(
                                subject=f'Новый комментарий к уроку: {lesson.title}',
                                message=f'''
                                Здравствуйте, {teacher.get_full_name() or teacher.username}!
                                
                                {comment.author.get_full_name() or comment.author.username} оставил комментарий к уроку "{lesson.title}":
                                
                                "{comment.text}"
                                
                                Курс: {lesson.course.title}
                                ''',
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[teacher.email],
                                fail_silently=True,
                            )
                except Lesson.DoesNotExist:
                    pass
        
        return f'Comment notification sent for comment {comment_id}'
    except Comment.DoesNotExist:
        return f'Comment {comment_id} not found'
    except Exception as e:
        return f'Error sending comment notification: {str(e)}'
