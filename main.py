import csv
import re
from pprint import pprint

# читаем файл
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# -------------------------------
# 1. Приведение ФИО
# -------------------------------
normalized_contacts = [contacts_list[0]]  # заголовок

for contact in contacts_list[1:]:
    full_name = " ".join(contact[:3]).split()

    lastname = full_name[0] if len(full_name) > 0 else ""
    firstname = full_name[1] if len(full_name) > 1 else ""
    surname = full_name[2] if len(full_name) > 2 else ""

    normalized_contacts.append([
        lastname,
        firstname,
        surname,
        contact[3],
        contact[4],
        contact[5],
        contact[6]
    ])

# -------------------------------
# 2. Приведение телефонов
# -------------------------------
phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?[\s\-]*"
    r"(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})"
    r"(?:\s*\(?(?:доб\.?)\s*(\d+)\)?)?"
)

def format_phone(phone):
    if not phone:
        return ""

    match = phone_pattern.search(phone)
    if not match:
        return phone  # если не распарсился — оставить как есть

    ext = match.group(6)
    if ext:
        ext = ext.lstrip("0")  # убираем ведущие нули

    formatted = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"

    if ext:
        formatted += f" доб.{ext}"

    return formatted

for contact in normalized_contacts[1:]:
    contact[5] = format_phone(contact[5])

# -------------------------------
# 3. Объединение дублей по ФИО
# -------------------------------
contacts_dict = {}

for contact in normalized_contacts[1:]:
    key = (contact[0], contact[1], contact[2])  # ФИО

    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        existing = contacts_dict[key]
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

# финальный список
final_contacts = [normalized_contacts[0]] + list(contacts_dict.values())

# вывод для проверки
pprint(final_contacts)

# -------------------------------
# 4. Запись в файл
# -------------------------------
with open("phonebook.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(final_contacts)