import re


def normalize_name(contact):
    full = " ".join(contact[:3]).strip()
    full = re.sub(r"\s+", " ", full)

    parts = full.split(" ")

    lastname = parts[0] if len(parts) > 0 else ""
    firstname = parts[1] if len(parts) > 1 else ""
    surname = parts[2] if len(parts) > 2 else ""

    return lastname, firstname, surname


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


def merge_contacts(contacts_list):
    result = {}
    header = contacts_list[0]

    for contact in contacts_list[1:]:
        lastname, firstname, surname = normalize_name(contact)
        phone = normalize_phone(contact[5])

        key = (lastname, firstname)

        new_contact = [
            lastname,
            firstname,
            surname,
            contact[3].strip(),
            contact[4].strip(),
            phone,
            contact[6].strip()
        ]

        if key not in result:
            result[key] = new_contact
        else:
            existing = result[key]
            for i in range(len(existing)):
                if not existing[i] and new_contact[i]:
                    existing[i] = new_contact[i]

    return [header] + list(result.values())