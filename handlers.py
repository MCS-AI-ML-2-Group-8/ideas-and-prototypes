from enum import Enum
from typing import Callable, List, Tuple
from contacts.book import AddressBook, RecordAlreadyExists, RecordNotFound
from contacts.records import PhoneAlreadyExists, PhoneNotFound, Record
from contacts.fields import ValidationException


class Result(Enum):
    """
    Possible command handler result statuses
    """
    SUCCESS = 0
    SUCCESS_DATA = 1
    WARNING = 2
    ERROR = 3


def handle_domain_error(handler: Callable):
    """
    Wraps command handler and handles domain exceptions
    """
    def inner(*args, **kwargs) -> Tuple[Result, str]:
        try:
            return handler(*args, **kwargs)
        
        except RecordNotFound:
            return Result.WARNING, "WARNING: Contact not found. Use 'add' command to add new contact"
            
        except RecordAlreadyExists:
            return Result.WARNING, "WARNING: Contact already exists. Use 'change' command to edit contact"
                    
        except (PhoneNotFound, PhoneAlreadyExists) as e:
            return Result.WARNING, f"WARNING: {e}"
            
        except ValidationException as e:
            return Result.ERROR, f"ERROR: {e}"

    return inner


@handle_domain_error
def add_contact(book: AddressBook, args: List) -> Tuple[Result, str]:
    """
    Adds contact to address book.
    Returns tuple: status, message
    """
    if len(args) != 2:
        return Result.ERROR, f"ERROR: 'add' command accepts two arguments: name and phone number. Provided {len(args)} value(s)"

    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return Result.SUCCESS, "Phone number added to existing contact."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return Result.SUCCESS, "Contact created."


@handle_domain_error
def change_contact(book: AddressBook, args: List) -> Tuple[Result, str]:
    """
    Changes contact in address book.
    Returns tuple: status, message
    """
    if len(args) != 3:
        return Result.ERROR, f"ERROR: 'change' command accepts three arguments: name, old phone number, new phone number. Provided {len(args)} value(s)"
    
    name, old_phone, new_phone = args
    record = book[name]
    record.edit_phone(old_phone, new_phone)
    return Result.SUCCESS, "Contact updated."


@handle_domain_error
def get_phones(book: AddressBook, args: List) -> Tuple[Result, str]:
    """
    Gets contact from address book.
    Returns tuple: status, contact phones representation
    """
    if len(args) != 1:
        return Result.ERROR, f"ERROR: 'phone' command accepts one argument: name. Provided {len(args)} value(s)"
    
    name = args[0]
    record = book[name]
    phones = [str(phone) for phone in record.phones]
    return Result.SUCCESS_DATA, "\n".join(phones)


@handle_domain_error
def add_birthday(book: AddressBook, args: List) -> Tuple[Result, str]:
    if len(args) != 2:
        return Result.ERROR, f"ERROR: 'add-birthday' command accepts two arguments: name and date of birth in 'DD.MM.YYYY' format. Provided {len(args)} value(s)"

    name, date_of_birth = args
    record = book[name]
    record.add_birthday(date_of_birth)
    return Result.SUCCESS, "Date of birth saved."


@handle_domain_error
def show_birthday(book: AddressBook, args: List) -> Tuple[Result, str]:
    if len(args) != 1:
        return Result.ERROR, f"ERROR: 'show-birthday' command accepts one argument: name. Provided {len(args)} value(s)"

    name = args[0]
    record = book[name]
    if record.birthday:
        return Result.SUCCESS_DATA, str(record.birthday)
    else:
        return Result.WARNING, "Birthday is not set"


@handle_domain_error
def get_upcoming_birthdays(book: AddressBook, args: list) -> Tuple[Result, str]:
    reminders = book.get_upcoming_birthdays(days_before_reminder=7)
    if len(reminders):
        result = [f"{reminder.name}: {reminder.date}" for reminder in reminders]
        return Result.SUCCESS_DATA, "\n".join(result)
    else:
        return Result.WARNING, "There is no upcoming birthdays this week"


def get_all(book: AddressBook, args: list) -> Tuple[Result, str]:
    """
    Returns all contacts from address book.
    Returns tuple: status, contacts text representation
    """
    if len(book) == 0:
        return Result.WARNING, "Contact book is empty"
    
    records = [str(record) for record in book.values()]
    return Result.SUCCESS_DATA, "\n".join(records)
