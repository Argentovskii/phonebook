import pytest
from phonebook import normalize_name, normalize_phone, merge_contacts


# -------------------------------
# Тест ФИО
# -------------------------------
@pytest.mark.parametrize(
    "input_data, expected",
    [
        (["Иванов Иван Иванович", "", ""], ("Иванов", "Иван", "Иванович")),
        (["Иванов", "Иван", "Иванович"], ("Иванов", "Иван", "Иванович")),
        (["Иванов Иван", "", ""], ("Иванов", "Иван", "")),
        (["  Иванов   Иван  Иванович  ", "", ""], ("Иванов", "Иван", "Иванович")),
    ]
)
def test_normalize_name(input_data, expected):
    assert normalize_name(input_data) == expected


# -------------------------------
# Тест телефонов
# -------------------------------
@pytest.mark.parametrize(
    "phone, expected",
    [
        ("8 999 123 45 67", "+7(999)123-45-67"),
        ("+7(999)123-45-67", "+7(999)123-45-67"),
        ("8(999)1234567", "+7(999)123-45-67"),
        ("8 999 123 45 67 доб.1234", "+7(999)123-45-67 доб.1234"),
        ("", ""),
    ]
)
def test_normalize_phone(phone, expected):
    assert normalize_phone(phone) == expected


# -------------------------------
# Тест объединения дублей
# -------------------------------
def test_merge_contacts():
    contacts = [
        ["lastname", "firstname", "surname", "org", "pos", "phone", "email"],

        ["Иванов", "Иван", "", "Компания", "", "", "ivan@mail.ru"],
        ["Иванов", "Иван", "", "", "Менеджер", "8 999 123 45 67", ""],
    ]

    result = merge_contacts(contacts)

    # ожидаем 2 строки (header + 1 контакт)
    assert len(result) == 2

    person = result[1]

    assert person[0] == "Иванов"
    assert person[1] == "Иван"
    assert person[3] == "Компания"
    assert person[4] == "Менеджер"
    assert person[5] == "+7(999)123-45-67"
    assert person[6] == "ivan@mail.ru"


# -------------------------------
# Тест: не затираются данные
# -------------------------------
def test_merge_does_not_overwrite():
    contacts = [
        ["lastname", "firstname", "surname", "org", "pos", "phone", "email"],

        ["Иванов", "Иван", "", "", "", "+7(999)111-11-11", ""],
        ["Иванов", "Иван", "", "", "", "", "ivan@mail.ru"],
    ]

    result = merge_contacts(contacts)
    person = result[1]

    assert person[5] == "+7(999)111-11-11"
    assert person[6] == "ivan@mail.ru"