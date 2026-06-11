import re
import csv
from pprint import pprint

# Чтение исходного файла
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

# Заголовок
header = contacts_list[0]
data = contacts_list[1:]

# Функция для нормализации ФИО
def normalize_name(row):
    # Объединяем первые три поля в строку и разбиваем по пробелам
    full_name = ' '.join(row[:3]).split()
    # Если получилось 3 части - всё хорошо
    while len(full_name) < 3:
        full_name.append('')  # добавляем пустые отчества при их отсутствии
    # Возвращаем нормализованные lastname, firstname, surname + остальные поля
    return full_name + row[3:]

# Нормализуем ФИО для всех записей
normalized = []
for row in data:
    normalized.append(normalize_name(row))

# Функция для приведения телефона к нужному формату
def format_phone(phone):
    if not phone:
        return ''
    # Ищем номер и доб. номер
    # Основной номер: 7,8, +7, 8-495... и т.п.
    pattern = r'(\+7|8)?\s*\(?(\d{3})\)?\s*[-]?(\d{3})[-]?(\d{2})[-]?(\d{2})'
    # Добавочный номер: доб. \d+
    ext_pattern = r'доб\.\s*(\d+)'
    # Замена основного номера на +7(XXX)XXX-XX-XX
    main = re.sub(pattern, r'+7(\2)\3-\4-\5', phone)
    # Поиск добавочного
    ext = re.search(ext_pattern, phone, re.IGNORECASE)
    if ext:
        main += f' доб.{ext.group(1)}'
    return main

# Применяем форматирование телефона
for row in normalized:
    row[5] = format_phone(row[5])

# Объединение дубликатов по фамилии и имени
contacts_dict = {}
for row in normalized:
    key = (row[0], row[1])  # фамилия + имя
    if key not in contacts_dict:
        contacts_dict[key] = row
    else:
        # Объединяем существующую и новую запись
        existing = contacts_dict[key]
        for i in range(len(row)):
            if row[i] and not existing[i]:
                existing[i] = row[i]
            # Для телефона, если оба не пустые, оставляем первый (по условию телефон один)
        contacts_dict[key] = existing

# Преобразуем словарь обратно в список, сохраняя заголовок
result = [header] + list(contacts_dict.values())

# Запись результата в новый CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)
print("Обработка исходного файла завершена, результат в phonebook.csv")