
"""
Celery tasks для courses приложения.
"""
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail, get_connection
from django.conf import settings
from datetime import timedelta

from .models import Assignment, Submission
from notifications.models import Notification


@shared_task
def send_assignment_deadline_reminder(assignment_id):
    """
    Отправить напоминание о приближающемся дедлайне задания.
    """
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        
        # Получаем студентов, записанных на курс
        enrolled_students = assignment.lesson.course.enrollments.filter(
            is_active=True
        ).select_related('student')
        
        for enrollment in enrolled_students:
            student = enrollment.student
            
            # Проверяем, не сдал ли уже студент задание
            has_submitted = Submission.objects.filter(
                assignment=assignment,
                student=student
            ).exists()
            
            if not has_submitted:
                # Создаем уведомление
                Notification.objects.create(
                    recipient=student,
                    notification_type='assignment_deadline',
                    title=f'Приближается дедлайн: {assignment.title}',
                    message=f'Задание "{assignment.title}" необходимо сдать до {assignment.due_date.strftime("%d.%m.%Y %H:%M")}',
                    content_object=assignment
                )
                
                # Отправляем email
                if student.email:
                    clean_email = student.email.strip().replace('\n', '').replace('\r', '')
                    with get_connection() as connection:
                        send_mail(
                            subject=f'Напоминание о дедлайне: {assignment.title}',
                            message=f'''
                            Здравствуйте, {student.get_full_name() or student.username}!
                            
                            Напоминаем, что приближается дедлайн сдачи задания "{assignment.title}".
                            Курс: {assignment.lesson.course.title}
                            Урок: {assignment.lesson.title}
                            Срок сдачи: {assignment.due_date.strftime("%d.%m.%Y %H:%M")}
                            
                            Пожалуйста, не забудьте сдать задание вовремя!
                            ''',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[clean_email],
                            fail_silently=False,
                            connection=connection
                        )
        
        return f'Reminder sent for assignment {assignment_id}'
    except Assignment.DoesNotExist:
        return f'Assignment {assignment_id} not found'
    except Exception as e:
        print(f"Error in send_assignment_deadline_reminder for assignment {assignment_id}: {e}")
        raise


@shared_task
def check_assignment_deadlines():
    """
    Периодическая задача для проверки приближающихся дедлайнов.
    Выполняется каждый час через Celery Beat.
    """
    now = timezone.now()
    # Проверяем задания с дедлайном через 24 часа
    deadline_time = now + timedelta(hours=24)
    
    assignments = Assignment.objects.filter(
        due_date__lte=deadline_time,
        due_date__gt=now
    )
    
    count = 0
    for assignment in assignments:
        # Запускаем задачу отправки напоминаний
        send_assignment_deadline_reminder.delay(assignment.id)
        count += 1
    
    return f'Checked {count} assignments'


@shared_task
def send_grade_notification(grade_id):
    """
    Отправить уведомление студенту о новой оценке.
    """
    from .models import Grade
    
    try:
        grade = Grade.objects.select_related(
            'submission__student',
            'submission__assignment',
            'graded_by'
        ).get(id=grade_id)
        
        student = grade.submission.student
        assignment = grade.submission.assignment
        
        # Создаем уведомление
        Notification.objects.create(
            recipient=student,
            notification_type='assignment_graded',
            title=f'Задание оценено: {assignment.title}',
            message=f'Ваше задание "{assignment.title}" оценено. Баллы: {grade.score}/{assignment.max_score}',
            content_object=grade
        )
        
        # Отправляем email
        if student.email:
            clean_email = student.email.strip().replace('\n', '').replace('\r', '')
            with get_connection() as connection:
                send_mail(
                    subject=f'Задание оценено: {assignment.title}',
                    message=f'''
                    Здравствуйте, {student.get_full_name() or student.username}!
                    
                    Ваше задание "{assignment.title}" было проверено.
                    
                    Курс: {assignment.lesson.course.title}
                    Урок: {assignment.lesson.title}
                    Баллы: {grade.score}/{assignment.max_score}
                    Преподаватель: {grade.graded_by.get_full_name() or grade.graded_by.username}
                    
                    {f"Комментарий: {grade.feedback}" if grade.feedback else ""}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[clean_email],
                    fail_silently=False,
                    connection=connection
                )
        
        return f'Grade notification sent for grade {grade_id}'
    except Exception as e:
        print(f"Error in send_grade_notification for grade {grade_id}: {e}")
        raise


@shared_task
def send_new_assignment_notification(assignment_id):
    """
    Отправить уведомление о новом задании всем студентам курса.
    """
    try:
        assignment = Assignment.objects.select_related(
            'lesson__course'
        ).get(id=assignment_id)
        
        # Получаем всех студентов курса
        enrolled_students = assignment.lesson.course.enrollments.filter(
            is_active=True
        ).select_related('student')
        
        for enrollment in enrolled_students:
            student = enrollment.student
            
            # Создаем уведомление
            Notification.objects.create(
                recipient=student,
                notification_type='new_assignment',
                title=f'Новое задание: {assignment.title}',
                message=f'Добавлено новое задание в курсе "{assignment.lesson.course.title}". Срок сдачи: {assignment.due_date.strftime("%d.%m.%Y %H:%M") if assignment.due_date else "не указан"}',
                content_object=assignment
            )
            
            # Отправляем email
            if student.email:
                clean_email = student.email.strip().replace('\n', '').replace('\r', '')
                with get_connection() as connection:
                    send_mail(
                        subject=f'Новое задание: {assignment.title}',
                        message=f'''
                        Здравствуйте, {student.get_full_name() or student.username}!
                        
                        В курсе "{assignment.lesson.course.title}" добавлено новое задание.
                        
                        Урок: {assignment.lesson.title}
                        Задание: {assignment.title}
                        {f"Срок сдачи: {assignment.due_date.strftime('%d.%m.%Y %H:%M')}" if assignment.due_date else ""}
                        
                        Описание:
                        {assignment.description}
                        ''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[clean_email],
                        fail_silently=False,
                        connection=connection
                    )
        
        return f'New assignment notification sent for {assignment_id}'
    except Assignment.DoesNotExist:
        return f'Assignment {assignment_id} not found'
    except Exception as e:
        print(f"Error in send_new_assignment_notification for assignment {assignment_id}: {e}")
        raise

