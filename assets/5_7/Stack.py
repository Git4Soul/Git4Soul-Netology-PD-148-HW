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


# Тесты

@pytest.fixture
def filled_stack():
    """Стек с 3 элементами."""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    return stack


def test_is_empty_on_new_stack():
    stack = Stack()
    assert stack.is_empty() is True


def test_is_empty_on_filled_stack(filled_stack):
    assert filled_stack.is_empty() is False


def test_push_increases_size():
    stack = Stack()
    stack.push(42)
    assert stack.size() == 1
    assert stack.peek() == 42


def test_push_multiple_items():
    stack = Stack()
    stack.push('a')
    stack.push('b')
    assert stack.size() == 2
    assert stack.peek() == 'b'


def test_pop_returns_and_removes_top(filled_stack):
    top = filled_stack.pop()
    assert top == 3
    assert filled_stack.size() == 2
    assert filled_stack.peek() == 2


def test_pop_on_empty_raises():
    stack = Stack()
    with pytest.raises(IndexError, match="pop from empty stack"):
        stack.pop()


def test_peek_returns_top_without_removing(filled_stack):
    top = filled_stack.peek()
    assert top == 3
    assert filled_stack.size() == 3  # размер не поменялся


def test_peek_on_empty_raises():
    stack = Stack()
    with pytest.raises(IndexError, match="peek from empty stack"):
        stack.peek()


def test_size_on_empty_stack():
    stack = Stack()
    assert stack.size() == 0


def test_size_after_operations(filled_stack):
    filled_stack.pop()
    filled_stack.push(100)
    assert filled_stack.size() == 3  # 3+1-1 = 3


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v"])