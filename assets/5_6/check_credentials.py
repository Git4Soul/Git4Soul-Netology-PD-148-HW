import pytest

def check_auth(login: str, password: str):

    if login == 'admin' and password == 'password':
        result = 'Добро пожаловать'
        # В этом блоке напишите код, который выполнится, если условие True. Используйте result, как в задании выше
    else:
        result = 'Доступ ограничен'
        # В этом блоке напишите код, который выполнится, если условие False. Используйте result, как в задании выше

    return result

@pytest.mark.parametrize(
    "login, password, expected",
    [
        ("admin", "password", "Добро пожаловать"),
        ("user", "password", "Доступ ограничен"),
        ("Admin", "password", "Доступ ограничен"),  # регистр имеет значение
        ("", "password", "Доступ ограничен"),
        ("admin", "pass", "Доступ ограничен"),
        ("admin", "Password", "Доступ ограничен"),
        ("admin", "", "Доступ ограничен"),
        ("user", "pass", "Доступ ограничен"),
        ("", "", "Доступ ограничен"),
        ("", "", "Доступ ограничен"),
        ("admin!", "password", "Доступ ограничен"),
        ("admin", "password!", "Доступ ограничен"),
    ]
)
def test_check_auth(login, password, expected):
    """Параметризованный тест для check_auth."""
    assert check_auth(login, password) == expected