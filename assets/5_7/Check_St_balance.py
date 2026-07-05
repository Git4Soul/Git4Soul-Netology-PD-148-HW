import pytest


class Stack:
    """
    Класс, реализующий стек LIFO.
    """

    def __init__(self):
        """Инициализирует пустой стек."""
        self._items = []

    def is_empty(self) -> bool:
        """Проверяет, пуст ли стек."""
        return len(self._items) == 0

    def push(self, item):
        """Добавляет элемент наверх стека."""
        self._items.append(item)

    def pop(self):
        """
        Удаляет и возвращает верхний элемент стека.
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """
        Возвращает верхний элемент без удаления.
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def size(self) -> int:
        """Возвращает количество эл-тов в стеке."""
        return len(self._items)


def is_balanced(s: str) -> bool:
    """
    Проверяет, сбалансированы ли скобки(учитывает только их) в строке:
    """
    opening = "([{"
    closing = ")]}"
    pairs = {')': '(', ']': '[', '}': '{'}

    stack = Stack()
    for ch in s:
        if ch in opening:
            stack.push(ch)
        elif ch in closing:
            if stack.is_empty():
                return False
            top = stack.pop()
            if top != pairs[ch]:
                return False
        # Любые другие символы игнорируются
    return stack.is_empty()


# Тесты
def test_balanced_sequences():
    assert is_balanced("(((([{}]))))") is True
    assert is_balanced("[([])((([[[]]])))]{()}") is True
    assert is_balanced("{{[()]}}") is True


def test_unbalanced_sequences():
    assert is_balanced("}{}") is False
    assert is_balanced("{{[(])]}}") is False
    assert is_balanced("[[{())}]") is False


if __name__ == "__main__":
    # Строку можно передать с помощью input или аргументом
    import sys
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Please enter a string with brackets: ")

    if is_balanced(user_input):
        print("Balanced")
    else:
        print("Unbalanced")