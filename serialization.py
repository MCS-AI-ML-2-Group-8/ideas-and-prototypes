import pickle
from pathlib import Path
from contacts.book import AddressBook
from handlers import Result
from output import print_status_message


def save_data(book: AddressBook, filename: str) -> None:
    try:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "wb") as f:
            pickle.dump(book, f)
            
    except OSError as e:
        print_status_message(Result.ERROR, f"Could not save file '{filename}': {e}")
    
    else:
        print_status_message(Result.SUCCESS, f"Changes saved to '{filename}'")


def load_data(filename: str) -> AddressBook:
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            print_status_message(Result.SUCCESS, f"Loaded '{filename}': {len(book)} contacts")
            return book

        
    except FileNotFoundError:
        print_status_message(Result.WARNING, f"File not found '{filename}'")
        return AddressBook()
    
    except Exception as e:
        print_status_message(Result.ERROR, f"Could not load file '{filename}': {e}")
        return AddressBook()
