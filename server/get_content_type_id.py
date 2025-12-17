"""
Скрипт для получения ContentType ID для модели Lesson.
Запустить: python manage.py shell < get_content_type_id.py
"""
from django.contrib.contenttypes.models import ContentType

try:
    lesson_ct = ContentType.objects.get(app_label='courses', model='lesson')
    print(f"\n=== ContentType ID для Lesson ===")
    print(f"ID: {lesson_ct.id}")
    print(f"App: {lesson_ct.app_label}")
    print(f"Model: {lesson_ct.model}")
    print(f"==================================\n")
except ContentType.DoesNotExist:
    print("ERROR: ContentType для courses.Lesson не найден!")
    print("Возможно, миграции не применены.")
