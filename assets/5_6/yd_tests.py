import os
import time
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()  # загружает токен из .env файла

TOKEN = os.getenv("YANDEX_DISK_TOKEN")
if not TOKEN:
    raise ValueError("Не задана переменная окружения YANDEX_DISK_TOKEN")

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"


@pytest.fixture
def folder_name():
    """Генерирует уникальное имя папки и удаляет её после теста."""
    name = f"test_folder_{int(time.time())}"
    yield name
    # teardown: удаляем папку после теста
    path = f"/{name}"
    headers = {"Authorization": f"OAuth {TOKEN}"}
    requests.delete(f"{BASE_URL}?path={path}", headers=headers)


@pytest.fixture
def headers():
    """Заголовки с авторизацией."""
    return {"Authorization": f"OAuth {TOKEN}"}


# Позитивные тесты

def test_create_folder_success(folder_name, headers):
    """Успешное создание папки — код ответа 201."""
    path = f"/{folder_name}"
    response = requests.put(f"{BASE_URL}?path={path}", headers=headers)

    assert response.status_code == 201, (
        f"Ожидался код 201, получен {response.status_code}. Ответ: {response.text}"
    )


def test_create_folder_appears_in_list(folder_name, headers):
    """Папка действительно появляется в списке файлов."""
    path = f"/{folder_name}"

    # Шаг 1: создаём папку
    requests.put(f"{BASE_URL}?path={path}", headers=headers)

    # Шаг 2: получаем список файлов в корне
    response = requests.get(f"{BASE_URL}?path=/", headers=headers)
    assert response.status_code == 200, "Не удалось получить список файлов"

    items = response.json().get("_embedded", {}).get("items", [])
    folder_names = [item["name"] for item in items if item.get("type") == "dir"]

    assert folder_name in folder_names, (
        f"Папка '{folder_name}' не найдена. Доступные папки: {folder_names}"
    )


# Негативные тесты

def test_create_folder_invalid_path(headers):
    """Ошибка 400 — попытка создать папку с пустым путём."""
    invalid_path = ""
    response = requests.put(f"{BASE_URL}?path={invalid_path}", headers=headers)
    assert response.status_code == 400


def test_create_folder_no_auth(folder_name):
    """Ошибка 401 — запрос без токена авторизации."""
    path = f"/{folder_name}"
    response = requests.put(f"{BASE_URL}?path={path}")  # без заголовка Authorization

    assert response.status_code == 401, (
        f"Ожидался код 401, получен {response.status_code}"
    )


def test_create_folder_already_exists(folder_name, headers):
    """Ошибка 409 — попытка создать уже существующую папку."""
    path = f"/{folder_name}"

    # Шаг 1: создаём папку
    requests.put(f"{BASE_URL}?path={path}", headers=headers)

    # Шаг 2: повторно отправляем тот же запрос
    response = requests.put(f"{BASE_URL}?path={path}", headers=headers)

    assert response.status_code == 409, (
        f"Ожидался код 409, получен {response.status_code}"
    )
    error_data = response.json()
    assert error_data.get("error") == "DiskPathPointsToExistentDirectoryError", (
        "Ожидалась ошибка о том, что папка уже существует"
    )
