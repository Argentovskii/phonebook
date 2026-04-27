import re


def normalize_name(contact):
    name_parts = []
    for field in contact[:3]:
        if field and field.strip():
            # Разбиваем по пробелам, чтобы собрать все части ФИО
            name_parts.extend([part.strip() for part in field.strip().split() if part.strip()])

    full_name = " ".join(name_parts).strip()
    full_name = re.sub(r"\s+", " ", full_name)

    parts = full_name.split()
    lastname = parts[0] if len(parts) > 0 else ""
    firstname = parts[1] if len(parts) > 1 else ""
    surname = parts[2] if len(parts) > 2 else ""

    return lastname, firstname, surname


phone_pattern = re.compile(
    r"(\+7|8)?[\s\(\-]*(\d{3})[\s\)\-\.]*"
    r"(\d{3})[\s\-\.]*(\d{2})[\s\-\.]*(\d{2})"
    r"(?:[\s\(\-]*(?:доб\.?|д\.?|доб|д)[\s\.]?(\d+))?",
    re.IGNORECASE
)


def normalize_phone(phone):
    if not phone or not str(phone).strip():
        return ""

    match = phone_pattern.search(str(phone))
    if not match:
        return str(phone).strip()

    g = match.groups()
    area = g[1]      # код региона
    num1 = g[2]
    num2 = g[3]
    num3 = g[4]
    ext = g[5]

    result = f"+7({area}){num1}-{num2}-{num3}"

    if ext:
        ext = ext.lstrip("0")
        result += f" доб.{ext}"

    return result


def merge_contacts(contacts_list):
    if not contacts_list or len(contacts_list) < 1:
        return []

    header = contacts_list[0]
    result = {}   # ключ: (lastname, firstname)

    for contact in contacts_list[1:]:
        lastname, firstname, surname = normalize_name(contact)

        # Защита от коротких строк
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