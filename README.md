Проект использует Django и Django Rest Framework (DRF) для создания RESTful API.

Основные шаги по установке, настройке и использованию API, а также описания доступных эндпоинтов.

Создание виртуального окружения

python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows


Установка зависимостей

pip install -r requirements.txt

Применение миграций
python manage.py makemigrations
python manage.py migrate

Swagger UI
http://127.0.0.1:8000/swagger/

Административная панель
http://127.0.0.1:8000/admin/


API Эндпоинты

1 Получение списка справочников

Параметры запроса:
-date (опционально)

GET /api/refbooks/?date=


2 Получение элементов для версии заданного справочника

GET /api/refbooks/1/elements/?version=

Параметры запроса:
-version (опционально): Версия справочника.


3 Валидация элемента справочника

Параметры запроса:
-code: Код элемента.
-value: Значение элемента.
-version (опционально): Версия справочника.

GET /api/refbooks/<id>/check_element?code=<code>&value=<value> [&version=<version>]
