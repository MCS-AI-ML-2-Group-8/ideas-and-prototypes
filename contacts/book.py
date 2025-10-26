from typing import Dict, List
from dataclasses import dataclass
from datetime import date, datetime
from collections import UserDict
from .records import Record


class RecordNotFound(Exception):
    """
    When record with this name was not found in address book,
    and can't de deleted
    """
    pass


class RecordAlreadyExists(Exception):
    """
    When record with same name already exists in address book,
    and can't be added
    """
    pass


@dataclass
class Reminder:
    name: str
    date: str


class AddressBook(UserDict):
    """
    Address book, wraps dictionary with name as a key, and Record as a value
    """
    data: Dict[str, Record]

    def add_record(self, record: Record) -> None:
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            raise RecordAlreadyExists()

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            self.data.pop(name)
        else:
            raise RecordNotFound()

    def get_upcoming_birthdays(self, days_before_reminder = 7) -> List[Reminder]:
        today = date.today()
        results = []
        for record in self.data.values():
            day = record.get_next_celebration_day()
            if day is None or (day - today).days > days_before_reminder:
                continue

            reminder = Reminder(
                name=str(record.name),
                date=datetime.strftime(day, "%d.%m.%Y")
            )
            results.append(reminder)
        return results
    
    def __getitem__(self, name: str) -> Record:
        record = self.find(name)
        if record:
            return record
        else:
            raise RecordNotFound()

    def __str__(self):
        return f"== Contact book ==\n{'\n'.join(str(c) for c in self.data.values())}"
