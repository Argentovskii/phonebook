import csv
from phonebook import merge_contacts

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

final_contacts = merge_contacts(contacts_list)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final_contacts)

print(" Создан phonebook.csv с", len(final_contacts), "строками.")