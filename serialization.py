import pickle
from pathlib import Path
from contacts.book import AddressBook


def save_data(book: AddressBook, filename: str) -> None:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str) -> AddressBook:
    with open(filename, "rb") as f:
        book = pickle.load(f)
        return book
