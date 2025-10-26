from typing import List
from datetime import date
from .fields import Birthday, Name, Phone


class PhoneNotFound(Exception):
    """
    When phone was not found in list of phones,
    and can't be edited or removed
    """
    pass


class PhoneAlreadyExists(Exception):
    """
    When phone number already exists in list of phones,
    and can't be added
    """
    pass


class Record:
    """
    Address book record, consists of name and list of phone numbers
    """
    name: Name
    phones: List[Phone]
    birthday: Birthday | None

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: str) -> None:
        phone = self.find_phone(phone_number)
        if not phone:
            self.phones.append(Phone(phone_number))
        else:
            raise PhoneAlreadyExists("Phone number is already added")

    def edit_phone(self, phone_number: str, new_phone_number: str) -> None:
        phone = self.find_phone(phone_number)
        if not phone:
            raise PhoneNotFound("Phone number is not found")
        new_phone = self.find_phone(new_phone_number)
        if new_phone:
            raise PhoneAlreadyExists("Phone number is already added")
        phone.set_value(new_phone_number)
        
    def remove_phone(self, phone_number: str) -> None:
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
        else:
            raise PhoneNotFound("Phone number is not found")

    def find_phone(self, phone_number: str) -> Phone | None:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_birthday(self, date_of_birth: str) -> None:
        self.birthday = Birthday(date_of_birth)

    def get_next_celebration_day(self) -> date | None:
        if self.birthday:
            return self.birthday.get_next_celebration_day()
        else:
            return None

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        birthday_after_pipe = f" | Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value} | Phones: {phones}{birthday_after_pipe}"
