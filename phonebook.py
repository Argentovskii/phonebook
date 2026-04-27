import re


def normalize_name(contact):
    """Нормализация ФИО из первых трёх полей."""
    name_parts = []
    for field in contact[:3]:
        if field and field.strip():
            name_parts.extend([p.strip() for p in field.strip().split() if p.strip()])

    full_name = " ".join(name_parts).strip()
    full_name = re.sub(r"\s+", " ", full_name)

    parts = full_name.split()
    lastname = parts[0] if len(parts) > 0 else ""
    firstname = parts[1] if len(parts) > 1 else ""
    surname = parts[2] if len(parts) > 2 else ""

    return lastname, firstname, surname


# Надёжный паттерн для телефона
phone_pattern = re.compile(
    r"(?:\+7|8)?[\s\(\-]*(\d{3})[\s\)\-\.]*"   # код региона
    r"(\d{3})[\s\-\.]*"                         # первые 3 цифры
    r"(\d{2})[\s\-\.]*"                         # следующие 2
    r"(\d{2})"                                  # последние 2
    r"(?:[\s\(\-]*(?:доб\.?|д\.?|доб|д)[\s\.]?(\d+))?",  # добавочный
    re.IGNORECASE
)


def normalize_phone(phone):
    """Приводит телефон к формату +7(495)913-04-78 доб.2926"""
    if not phone or not str(phone).strip():
        return ""

    match = phone_pattern.search(str(phone))
    if not match:
        return str(phone).strip()

    area, num1, num2, num3, ext = match.groups()

    result = f"+7({area}){num1}-{num2}-{num3}"

    if ext:
        result += f" доб.{ext}"

    return result


def merge_contacts(contacts_list):
    """Объединяет дубли по (фамилия, имя), дозаполняя пустые поля."""
    if not contacts_list or len(contacts_list) < 1:
        return []

    header = contacts_list[0]
    result = {}

    for contact in contacts_list[1:]:
        lastname, firstname, surname = normalize_name(contact)

        org = contact[3].strip() if len(contact) > 3 else ""
        pos = contact[4].strip() if len(contact) > 4 else ""
        phone = normalize_phone(contact[5] if len(contact) > 5 else "")
        email = contact[6].strip() if len(contact) > 6 else ""

        key = (lastname, firstname)

        new_contact = [lastname, firstname, surname, org, pos, phone, email]

        if key not in result:
            result[key] = new_contact
        else:
            existing = result[key]
            for i in range(len(existing)):
                if not existing[i] and new_contact[i]:
                    existing[i] = new_contact[i]

    return [header] + list(result.values())