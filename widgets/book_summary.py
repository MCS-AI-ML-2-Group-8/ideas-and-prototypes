from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from contacts.book import AddressBook


class BookSummary(QWidget):
    def __init__(self, book: AddressBook):
        super().__init__()
        layout = QVBoxLayout()
        
        label = QLabel("Welcome!")
        label.setProperty("class", "text-primary text-xl")
        layout.addWidget(label)

        count_label = QLabel("Number of contacts:")
        count_label.setProperty("class", "text-primary")
        layout.addWidget(count_label)

        count_text = QLabel(f"{len(book)}")
        count_text.setProperty("class", "text-secondary")
        layout.addWidget(count_text)

        bidthdays_this_week = book.get_upcoming_birthdays(days_before_reminder=7)

        if bidthdays_this_week:
            bidthday_label = QLabel("Birthdays this week:")
            bidthday_label.setProperty("class", "text-primary")
            layout.addWidget(bidthday_label)

        for bidthday in bidthdays_this_week:
            bidthday_text = QLabel(f"{bidthday.name}: {bidthday.date}")
            bidthday_text.setProperty("class", "text-secondary")
            layout.addWidget(bidthday_text)

        layout.addStretch()
        self.setLayout(layout)
