import csv
import re
from pprint import pprint

# читаем файл
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]

# -------------------------------
# 1. НОРМАЛИЗАЦИЯ ФИО
# -------------------------------
def normalize_name(contact):
    # склеиваем и чистим лишние пробелы
    full = " ".join(contact[:3]).strip()
    full = re.sub(r"\s+", " ", full)

    parts = full.split(" ")

    lastname = parts[0] if len(parts) > 0 else ""
    firstname = parts[1] if len(parts) > 1 else ""
    surname = parts[2] if len(parts) > 2 else ""

    return lastname, firstname, surname


# -------------------------------
# 2. НОРМАЛИЗАЦИЯ ТЕЛЕФОНА
# -------------------------------
phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?[\s\-]*"
    r"(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})"
    r"(?:\s*\(?(?:доб\.?)\s*(\d+)\)?)?"
)

def normalize_phone(phone):
    if not phone:
        return ""

    match = phone_pattern.search(phone)
    if not match:
        return phone.strip()

    ext = match.group(6)
    if ext:
        ext = ext.lstrip("0")

    result = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"

    if ext:
        result += f" доб.{ext}"

    return result


# -------------------------------
# 3. ОБЪЕДИНЕНИЕ ДУБЛЕЙ
# -------------------------------
contacts_dict = {}

for contact in contacts_list[1:]:
    lastname, firstname, surname = normalize_name(contact)

    organization = contact[3].strip()
    position = contact[4].strip()
    phone = normalize_phone(contact[5])
    email = contact[6].strip()

    key = (lastname, firstname, surname)

    new_data = [
        lastname,
        firstname,
        surname,
        organization,
        position,
        phone,
        email
    ]

    if key not in contacts_dict:
        contacts_dict[key] = new_data
    else:
        existing = contacts_dict[key]

        # ДОЗАПОЛНЕНИЕ (главное место исправления)
        for i in range(len(existing)):
            if not existing[i] and new_data[i]:
                existing[i] = new_data[i]


# -------------------------------
# 4. ФИНАЛЬНЫЙ СПИСОК
# -------------------------------
final_contacts = [header] + list(contacts_dict.values())

# удалим полностью пустые строки (на всякий случай)
final_contacts = [row for row in final_contacts if any(field.strip() for field in row)]

# проверка
print("Было строк:", len(contacts_list))
print("Стало строк:", len(final_contacts))

pprint(final_contacts)


# -------------------------------
# 5. СОХРАНЕНИЕ
# -------------------------------
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final_contacts)