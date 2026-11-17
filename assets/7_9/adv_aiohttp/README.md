# REST API для объявлений (aiohttp)

Для запуска требуется Docker и Docker Compose.

### Запуск

Сборка и запуск контейнеров:

```bash
docker compose up --build -d
```

Сервер будет доступен по адресу http://127.0.0.1:8080

### Тестирование

Проверка работы API через client.py (надо поставить asyncio и aiohttp):

```bash
python client.py
```