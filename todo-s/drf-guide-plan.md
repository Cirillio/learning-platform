# План написания гайда по Django REST Framework (DRF)

Этот план составлен на основе запроса для создания исчерпывающего руководства для Frontend-разработчика.

- [ ] **1. Введение и Ментальная модель**

  - [ ] Определение REST и роль DRF.
  - [ ] Связь сущностей: Model -> Serializer -> View -> URL.
  - [ ] ASCII-схема жизненного цикла запроса.

- [ ] **2. Структура проекта и файлы**

  - [ ] Разбор `settings.py`, `urls.py`, `wsgi/asgi.py`.
  - [ ] Зачем нужны `apps.py`, `admin.py`, `migrations/`.
  - [ ] Правильная структура приложения: `serializers.py`, `services.py`, `selectors.py`.

- [ ] **3. ORM и Модели (Data Layer)**

  - [ ] Миграции: суть и процесс.
  - [ ] Связи (OneToMany, ManyToMany) и их отражение в БД.
  - [ ] Оптимизация: `select_related` vs `prefetch_related`.

- [ ] **4. Сериализаторы (Data Transfer Layer)**

  - [ ] Сериализатор как "переводчик" и валидатор.
  - [ ] `ModelSerializer` vs `Serializer`.
  - [ ] Валидация (`validate_<field>`, `validate`).
  - [ ] Вложенные сериализаторы.

- [ ] **5. Views и Routing (Interface Layer)**

  - [ ] Иерархия: `APIView` -> `GenericAPIView` -> `ViewSet`.
  - [ ] `ModelViewSet` и магия роутеров.
  - [ ] Таблица выбора View.

- [ ] **6. Request & Response**

  - [ ] Объект `request` (data, user, query_params).
  - [ ] HTTP статусы и Content Negotiation.

- [ ] **7. Безопасность: Auth & Permissions**

  - [ ] Authentication (кто ты?) vs Permissions (что можно?).
  - [ ] Типы аутентификации (Session, Token, JWT).

- [ ] **8. Дополнительные возможности**

  - [ ] Фильтрация, Поиск, Сортировка.
  - [ ] Пагинация.

- [ ] **9. Качество кода и Тестирование**

  - [ ] Обработка ошибок и исключений.
  - [ ] Тестирование с `APIClient`.

- [ ] **10. Заключение**
  - [ ] Чек-лист для самопроверки.
  - [ ] Типичные ошибки новичков.
  - [ ] План дальнейшего развития.
