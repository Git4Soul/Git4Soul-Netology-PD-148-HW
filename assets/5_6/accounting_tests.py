import unittest

from acconting_func import (
    get_name_by_number, show_documents, get_directory_by_number,
    add_document, remove_document
)


class TestDocumentFunctions(unittest.TestCase):

    def setUp(self):
        """Сбрасываем значения перед каждым тестом."""
        # Используем копии исходных данных, чтобы не менять оригинал
        self.docs = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]
        self.dirs = {
            '1': ['2207 876234', '11-2'],
            '2': ['10006'],
            '3': []
        }

    # Тесты для get_name_by_number
    def test_get_name_by_number_existing(self):
        name = get_name_by_number("2207 876234", self.docs)
        self.assertEqual(name, "Василий Гупкин")

    def test_get_name_by_number_not_existing(self):
        name = get_name_by_number("999", self.docs)
        self.assertIsNone(name)

    # Тесты для show_documents
    def test_show_documents(self):
        expected = (
            "passport 2207 876234 Василий Гупкин\n"
            "invoice 11-2 Геннадий Покемонов\n"
            "insurance 10006 Аристарх Павлов\n"
            "1 -> ['2207 876234', '11-2']\n"
            "2 -> ['10006']\n"
            "3 -> []"
        )
        result = show_documents(self.docs, self.dirs)
        self.assertEqual(result, expected)

    # Тесты для get_directory_by_number
    def test_get_directory_by_number_existing(self):
        shelf = get_directory_by_number("10006", self.dirs)
        self.assertEqual(shelf, "2")

    def test_get_directory_by_number_not_existing(self):
        shelf = get_directory_by_number("999", self.dirs)
        self.assertIsNone(shelf)

    # Тесты для add_document
    def test_add_document_to_existing_shelf(self):
        success = add_document("123", "Иван Петров", "passport", "1", self.docs, self.dirs)
        self.assertTrue(success)
        # проверяем, что документ добавился
        self.assertIn({"type": "passport", "number": "123", "name": "Иван Петров"}, self.docs)
        # проверяем, что номер появился на полке "1"
        self.assertIn("123", self.dirs["1"])

    def test_add_document_to_new_shelf(self):
        success = add_document("456", "Сергей Смирнов", "invoice", "5", self.docs, self.dirs)
        self.assertTrue(success)
        self.assertIn({"type": "invoice", "number": "456", "name": "Сергей Смирнов"}, self.docs)
        self.assertIn("5", self.dirs)
        self.assertIn("456", self.dirs["5"])

    def test_add_document_missing_data(self):
        success = add_document("", "Имя", "type", "1", self.docs, self.dirs)
        self.assertFalse(success)
        # данные не должны измениться
        self.assertEqual(len(self.docs), 3)

    # Тесты для remove_document
    def test_remove_document_existing(self):
        success, shelf = remove_document("11-2", self.docs, self.dirs)
        self.assertTrue(success)
        self.assertEqual(shelf, "1")
        # проверяем, что документ удалён из списка
        self.assertNotIn({"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"}, self.docs)
        # проверяем, что номер убран с полки
        self.assertNotIn("11-2", self.dirs["1"])

    def test_remove_document_not_existing(self):
        success, shelf = remove_document("999", self.docs, self.dirs)
        self.assertFalse(success)
        self.assertIsNone(shelf)
        # структуры не изменились
        self.assertEqual(len(self.docs), 3)

    def test_remove_document_orphan_on_shelf(self):
        # случай, когда документ есть на полке, но отсутствует в списке (редко, но проверим)
        # добавим номер в полку, но не в документы
        self.dirs["1"].append("777")
        success, shelf = remove_document("777", self.docs, self.dirs)
        self.assertFalse(success)  # т.к. в списке документов его нет
        self.assertEqual(shelf, "1")  # но с полки он убран
        self.assertNotIn("777", self.dirs["1"])


if __name__ == '__main__':
    unittest.main()