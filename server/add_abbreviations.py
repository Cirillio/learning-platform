#!/usr/bin/env python
"""Скрипт для добавления аббревиатур к курсам"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Course

# Маппинг: ID курса -> аббревиатура
ABBREVIATIONS = {
    8: 'Py',           # Python для начинающих
    9: 'JS',           # JavaScript: основы
    10: 'TS',          # TypeScript для профи
    11: 'DjREST',      # Django REST Framework
    12: 'Vue',         # Vue.js 3 + Composition API
    13: 'NuxtFS',      # Nuxt 3: Full-Stack
    14: 'HTML/CSS',    # HTML/CSS: с нуля до PRO
    15: 'Pandas',      # Pandas и NumPy
    16: 'ML',          # Machine Learning: основы
    17: 'DL',          # Deep Learning с PyTorch
    18: 'Flutter',     # Flutter для начинающих
    19: 'RN+',         # React Native: продвинутый
    20: 'Docker',      # Docker и Kubernetes
    21: 'CI/CD',       # CI/CD с GitHub Actions
    22: 'Figma',       # Figma: UI/UX дизайн
    23: 'DS',          # Дизайн-системы
    24: 'SMM',         # SMM с нуля
    25: 'Agile',       # Agile и Scrum
    26: 'DjAPI',       # Django Fast Api
}

def add_abbreviations():
    """Добавляет аббревиатуры к курсам"""
    updated_count = 0
    
    for course_id, abbr in ABBREVIATIONS.items():
        try:
            course = Course.objects.get(id=course_id)
            course.abbr = abbr
            course.save(update_fields=['abbr'])
            print(f'✓ {course.title}: {abbr}')
            updated_count += 1
        except Course.DoesNotExist:
            print(f'✗ Курс с ID {course_id} не найден')
    
    print(f'\nОбновлено курсов: {updated_count}/{len(ABBREVIATIONS)}')

if __name__ == '__main__':
    add_abbreviations()
