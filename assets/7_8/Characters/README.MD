# Выгрузка по API персонажей с загрузкой в БД

Для запуска требуется Docker и Docker Compose.

### Запуск

Собрать образ:
```bash
docker compose build
```

Выполнить миграцию:
```bash
docker compose run --rm app python migrate.py
```

Загрузить данные:
```bash
docker compose run --rm app python load_data.py
```