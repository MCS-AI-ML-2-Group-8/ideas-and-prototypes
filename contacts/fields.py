from typing import Any
from datetime import datetime, date, timedelta


class ValidationException(Exception):
    """
    Base validation exception
    """
    pass


class InvalidPhoneNumber(ValidationException):
    """
    When phone number has invalid format
    """
    pass


class InvalidBirthdayDate(ValidationException):
    """
    When birthday date has invalid format
    """
    pass


class Field:
    """
    Generic field
    """

    def __init__(self, value: Any):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Field for name in address book record
    """
    value: str


class Phone(Field):
    """
    Field for phone number in address book record
    """
    value: str

    def __init__(self, value: str):
        if not Phone.is_valid(value):
            raise InvalidPhoneNumber("Phone number must consist of exactly 10 digits")

        super().__init__(value)

    def set_value(self, value: str):
        if not Phone.is_valid(value):
            raise InvalidPhoneNumber("Phone number must consist of exactly 10 digits")

        self.value = value

    @staticmethod
    def is_valid(value: str) -> bool:
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    """
    Represent birthday date field
    """
    value: date

    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise InvalidBirthdayDate("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y")

    def get_next_celebration_day(self) -> date:
        """
        Returns celebration day on current year or next.
        """
        today = date.today()
        dob = self.value
        birthday = date(today.year, dob.month, dob.day)
        # Get celebration date before comparison with today:
        # If birthday is on Saturday, and today is Sunday - we still can congratulate on Monday
        celebration = Birthday.get_workday_celebration_day_for(birthday)
        if celebration >= today:
            return celebration
        else:
            # If celebration date passed - congratulation comes next year
            birthday = date(today.year + 1, dob.month, dob.day)
            celebration = Birthday.get_workday_celebration_day_for(birthday)
            return celebration
        
    @staticmethod
    def get_workday_celebration_day_for(birthday: date) -> date:
        """
        Returns celebration day from birthday by shifting it away from weekend:
        Saturday to Monday,
        Sunday to Monday
        """
        weekday = birthday.isoweekday()
        shift = 0 if weekday not in [6, 7] else (8 - weekday)
        return birthday + timedelta(days=shift)
