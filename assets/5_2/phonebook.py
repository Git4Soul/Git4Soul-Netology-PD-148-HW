import re
import csv
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

header = contacts_list[0]
data = contacts_list[1:]

def normalize_name(row):
    full_name = ' '.join(row[:3]).split()
    while len(full_name) < 3:
        full_name.append('')
    return full_name + row[3:]

normalized = []
for row in data:
    normalized.append(normalize_name(row))

def format_phone(phone):
    if not phone:
        return ''
    # Извлекаем добавочный номер, учитывая возможные скобки
    ext_match = re.search(r'(?:\(?доб\.?\s*(\d+)\)?)', phone, re.IGNORECASE)
    ext = ext_match.group(1) if ext_match else None
    # Удаляем добавочный номер вместе со скобками и пробелами
    phone_clean = re.sub(r'\(?доб\.?\s*\d+\)?', '', phone, flags=re.IGNORECASE)
    # Удаляем оставшиеся пустые скобки
    phone_clean = re.sub(r'\(\)', '', phone_clean)
    phone_clean = phone_clean.strip()
    # Форматируем основной номер
    pattern = r'(\+7|8)?\s*\(?(\d{3})\)?\s*[-]?(\d{3})[-]?(\d{2})[-]?(\d{2})'
    formatted = re.sub(pattern, r'+7(\2)\3-\4-\5', phone_clean)
    if ext:
        formatted += f' доб.{ext}'
    return formatted

for row in normalized:
    row[5] = format_phone(row[5])

contacts_dict = {}
for row in normalized:
    key = (row[0], row[1])
    if key not in contacts_dict:
        contacts_dict[key] = row
    else:
        existing = contacts_dict[key]
        for i in range(len(row)):
            if row[i] and not existing[i]:
                existing[i] = row[i]
        contacts_dict[key] = existing

result = [header] + list(contacts_dict.values())

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)
print("Обработка завершена. Результат в phonebook.csv")