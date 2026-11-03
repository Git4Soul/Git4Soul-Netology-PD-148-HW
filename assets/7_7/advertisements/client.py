import requests
import json

BASE_URL = "http://127.0.0.1:5000"
ADS_URL = f"{BASE_URL}/advertisements"


def print_response(response):
    """Вспомогательная функция для красивого вывода ответов"""
    print(f"Статус-код: {response.status_code}")
    try:
        print(f"Ответ: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")
    except requests.exceptions.JSONDecodeError:
        print(f"Ответ (текст): {response.text}")
    print("-" * 50)


if __name__ == "__main__":
    print("1. ТЕСТИРОВАНИЕ МЕТОДА POST (Создание объявления)")
    new_ad = {
        "title": "Продам велосипед",
        "description": "Горный, 21 скорость, в отличном состоянии",
        "owner": "Дмитрий"
    }
    response = requests.post(ADS_URL, json=new_ad)
    print_response(response)

    ad_id = response.json().get("id") if response.status_code == 201 else None

    if ad_id:
        print("2. ТЕСТИРОВАНИЕ МЕТОДА GET (Получение списка всех объявлений)")
        response = requests.get(ADS_URL)
        print_response(response)

        print(f"3. ТЕСТИРОВАНИЕ МЕТОДА PATCH (Редактирование объявления ID={ad_id})")
        update_data = {
            "title": "Продам велосипед (СРОЧНО)",
            "description": "Торг возможен"
        }
        response = requests.patch(f"{ADS_URL}/{ad_id}", json=update_data)
        print_response(response)

        print(f"4. ТЕСТИРОВАНИЕ МЕТОДА GET (Получение одного объявления ID={ad_id})")
        response = requests.get(f"{ADS_URL}/{ad_id}")
        print_response(response)

        print(f"5. ТЕСТИРОВАНИЕ МЕТОДА DELETE (Удаление объявления ID={ad_id})")
        response = requests.delete(f"{ADS_URL}/{ad_id}")
        print_response(response)

        print(f"6. ПРОВЕРКА (Попытка получить удаленное объявление ID={ad_id})")
        response = requests.get(f"{ADS_URL}/{ad_id}")
        print_response(response)  # Ожидаем 404
    else:
        print("Не удалось создать объявление. ")