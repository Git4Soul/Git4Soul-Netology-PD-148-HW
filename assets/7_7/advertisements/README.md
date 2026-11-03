# REST API для объявлений (Flask)

Для запуска требуется Docker и Docker Compose.

### Запуск

1. Переименуйте файл `.env.example` в `.env`. 
2. Соберите и запустите контейнеры:
```bash
docker compose up --build -d

Сервер будет доступен по адресу: http://127.0.0.1:5000

### Тестирование

python client.py