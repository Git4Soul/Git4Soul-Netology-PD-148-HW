# Stocks Products API
Бэкенд-сервер для управления товарами и логистикой, разработанный на Django и Django REST Framework (DRF).


## Технические особенности

Язык: Python 3.9.14
Фреймворк: Django, Django REST Framework (DRF)
База данных: SQLite (встроена в проект)
Контейнеризация: Docker


## Полезные команды Docker для работы с проектом

1. Сборка Docker-образа:

```bash
docker build -t stocks-backend .
```

2. Запуск контейнера в фоновом режиме с пробросом порта 8000:

```bash
docker run -d -p 8000:8000 --name stocks-container stocks-backend
```

3. Просмотр логов сервера:

```bash
docker logs -f stocks-container
```

## Проверка работы API
requests-examples.http — примеры HTTP-запросов к API.