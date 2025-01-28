# Django Testing Project

Проект содержит набор тестов для двух Django-приложений: YaNote (заметки) и YaNews (новостной сайт). В проекте реализовано тестирование с использованием двух фреймворков: unittest и pytest.

## Структура проекта

```
Dev
 └── django_testing
     ├── ya_news/                    # Проект YaNews
     │   ├── news/                   # Приложение news
     │   │   ├── pytest_tests/       # Тесты pytest
     │   │   └── ...
     │   ├── templates/
     │   └── manage.py
     │
     ├── ya_note/                    # Проект YaNote
     │   ├── notes/                  # Приложение notes
     │   │   ├── tests/             # Тесты unittest
     │   │   └── ...
     │   ├── templates/
     │   └── manage.py
     │
     └── requirements.txt            # Зависимости проекта
```

## Тестовое покрытие

### YaNote (unittest)
1. Тестирование маршрутов (`test_routes.py`):
   - Доступность страниц для разных типов пользователей
   - Проверка авторизации
   - Проверка прав доступа к заметкам

2. Тестирование контента (`test_content.py`):
   - Корректность передачи данных в шаблоны
   - Изоляция заметок между пользователями
   - Проверка форм

3. Тестирование логики (`test_logic.py`):
   - Создание заметок
   - Уникальность slug
   - Редактирование и удаление заметок

### YaNews (pytest)
1. Тестирование маршрутов (`test_routes.py`):
   - Доступность страниц новостей
   - Права доступа к комментариям
   - Проверка авторизации

2. Тестирование контента (`test_content.py`):
   - Пагинация новостей
   - Сортировка новостей и комментариев
   - Доступность формы комментариев

3. Тестирование логики (`test_logic.py`):
   - Создание комментариев
   - Модерация комментариев
   - Управление комментариями

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <ваш-репозиторий>
cd django_testing
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запуск тестов YaNote:
```bash
cd ya_note
python manage.py test
```

5. Запуск тестов YaNews:
```bash
cd ya_news
pytest
```

## Технологии
- Python 3.9
- Django
- unittest
- pytest
- pytest-django
- pytils (для генерации slug)

## Автор
Соколов Григорий
