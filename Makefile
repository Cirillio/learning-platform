.PHONY: help build up down restart logs migrate shell test celery celery-beat clean dev-frontend dev-backend dev-celery dev-celery-beat dev dev-full

help:
	@echo "University Portal - Команды управления"
	@echo ""
	@echo "Docker команды:"
	@echo "make build       - Собрать Docker образы"
	@echo "make up          - Запустить все сервисы"
	@echo "make down        - Остановить все сервисы"
	@echo "make restart     - Перезапустить все сервисы"
	@echo "make logs        - Показать логи всех сервисов"
	@echo "make migrate     - Применить миграции Django"
	@echo "make shell       - Открыть Django shell"
	@echo "make superuser   - Создать суперпользователя"
	@echo "make test        - Запустить тесты"
	@echo "make celery      - Запустить Celery worker в контейнере"
	@echo "make celery-beat - Запустить Celery beat в контейнере"
	@echo "make clean       - Удалить все контейнеры и volumes"
	@echo ""
	@echo "Локальные команды:"
	@echo "make dev-frontend - Запустить фронтенд локально (pnpm dev)"
	@echo "make dev-backend  - Запустить бэкенд локально (python manage.py runserver)"
	@echo "make dev-celery   - Запустить Celery worker локально"
	@echo "make dev-celery-beat - Запустить Celery beat локально"
	@echo "make dev          - Запустить фронтенд и бэкенд локально параллельно"
	@echo "make dev-full     - Запустить фронтенд, бэкенд и Celery локально параллельно"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend python manage.py migrate

shell:
	docker-compose exec backend python manage.py shell

superuser:
	docker-compose exec backend python manage.py createsuperuser

test:
	docker-compose exec backend python manage.py test

celery:
	docker-compose exec celery_worker celery -A config worker -l info

celery-beat:
	docker-compose exec celery_beat celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

clean:
	docker-compose down -v
	docker system prune -f

# Локальные команды разработки
dev-frontend:
	cd client && pnpm dev

dev-backend:
	cd server && . ./virtenv/bin/activate && python3 manage.py runserver

dev-celery:
	cd server && . ./virtenv/bin/activate && celery -A config worker -l info

dev-celery-beat:
	cd server && . ./virtenv/bin/activate && celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

dev:
	@echo "Запуск фронтенда и бэкенда локально..."
	@make -j2 dev-frontend dev-backend

dev-full:
	@echo "Запуск фронтенда, бэкенда и Celery локально..."
	@make -j3 dev-frontend dev-backend dev-celery
