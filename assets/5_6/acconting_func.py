documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def get_name_by_number(number, docs):
    """
    Возвращает имя владельца документа или None, если документ не найден.
    """
    for doc in docs:
        if doc['number'] == number:
            return doc['name']
    return None


def show_documents(docs, dirs):
    """
    Возвращает строковое представление всех документов и полок.
    """
    lines = []
    for doc in docs:
        lines.append(f"{doc['type']} {doc['number']} {doc['name']}")
    for key, values in dirs.items():
        lines.append(f"{key} -> {values}")
    return "\n".join(lines)


def get_directory_by_number(number, dirs):
    """
    Возвращает номер полки, на которой лежит документ, или None, если не найден.
    """
    for directory, list_docs in dirs.items():
        if number in list_docs:
            return directory
    return None


def add_document(number, name, doc_type, directory_number, docs, dirs):
    """
    Добавляет новый документ и размещает его на указанной полке.
    """
    if not all([number, name, doc_type, directory_number]):
        return False

    # добавляем документ
    docs.append({"type": doc_type, "number": number, "name": name})

    # добавляем номер на полку (если полки нет – создаём)
    if directory_number in dirs:
        dirs[directory_number].append(number)
    else:
        dirs[directory_number] = [number]

    return True


def remove_document(person_number, docs, dirs):
    """
    Удаляет документ из списка и с соответствующей полки.
    """
    doc_removed = False
    for i, elem in enumerate(docs):
        if elem['number'] == person_number:
            docs.pop(i)
            doc_removed = True
            break

    shelf_found = None
    for shelf, numbers in dirs.items():
        if person_number in numbers:
            numbers.remove(person_number)
            shelf_found = shelf
            break

    # Успех только если документ реально присутствовал в списке
    if doc_removed:
        return True, shelf_found
    else:
        return False, shelf_found