from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contacts.book import Reminder
from contacts.fields import Phone
from contacts.records import Record
from serialization import load_data


filename = "./data/addressbook.pkl"
book = load_data(filename)
app = FastAPI()


class ReminderModel(BaseModel):
    name: str
    date: str

class PhoneModel(BaseModel):
    number: str = Field(..., pattern=r"\d{10}")

class ContactModel(BaseModel):
    name: str = Field(..., min_length=1)
    phones: list[PhoneModel]
    birthday: date | None


def map_reminder(reminder: Reminder) -> ReminderModel:
    return ReminderModel(
        name = reminder.name,
        date = reminder.date)

def map_phone(phone: Phone) -> PhoneModel:
    return PhoneModel(
        number = phone.value)

def map_contact(contact: Record) -> ContactModel:
    return ContactModel(
        name = str(contact.name),
        phones = list(map(map_phone, contact.phones)),
        birthday = contact.birthday.value if contact.birthday else None)


@app.get("/contacts/find")
def get_contact(name: str) -> ContactModel | None:
    contact = book.get(name)
    if contact:
        return map_contact(contact)
    else:
        raise HTTPException(404, "Contact not found")

@app.get("/contacts")
def get_contacts() -> list[ContactModel]:
    return list(map(map_contact, book.values()))

@app.get("/birthdays/upcoming")
def get_upcoming_birthdays(days_before_reminder: int = 7) -> list[ReminderModel]:
    reminders = book.get_upcoming_birthdays(days_before_reminder=days_before_reminder)
    return list(map(map_reminder, reminders))
