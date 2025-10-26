from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from contacts.records import Record


class ContactDetails(QWidget):
    deleteClicked = Signal(Record)
    editClicked = Signal(Record)

    def __init__(self, contact: Record):
        super().__init__()
        layout = QVBoxLayout()
        
        label = QLabel(str(contact.name))
        label.setProperty("class", "text-primary text-xl")
        layout.addWidget(label)

        current_phone = QLabel(str(contact.phones[0]))
        current_phone.setProperty("class", "text-secondary")
        layout.addWidget(current_phone)

        if len(contact.phones) > 1:
            additional_phones_label = QLabel("Additional phone numbers:")
            additional_phones_label.setProperty("class", "text-primary")
            layout.addWidget(additional_phones_label)

        for phone in contact.phones[1:]:
            additional_phone = QLabel(str(phone))
            additional_phone.setProperty("class", "text-secondary")
            layout.addWidget(additional_phone)

        if contact.birthday:
            birthday_label = QLabel("Birthday:")
            birthday_label.setProperty("class", "text-primary")
            layout.addWidget(birthday_label)

            birthday_text = QLabel(str(contact.birthday))
            birthday_text.setProperty("class", "text-secondary")
            layout.addWidget(birthday_text)

        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(120, 40)
        delete_button.setProperty("variant", "secondary")
        delete_button.clicked.connect(lambda: self.deleteClicked.emit(contact))

        edit_button = QPushButton("Edit contact")
        edit_button.setFixedSize(120, 40)
        edit_button.clicked.connect(lambda: self.editClicked.emit(contact))

        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(edit_button)

        layout.addStretch()
        layout.addWidget(buttons)

        self.setLayout(layout)
