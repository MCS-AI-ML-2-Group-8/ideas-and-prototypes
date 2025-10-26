from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from contacts.records import Record


class ContactListItem(QWidget):
    def __init__(self, contact: Record):
        super().__init__()
        self.contact = contact
        layout = QVBoxLayout()
        label = QLabel(str(contact.name))
        label.setProperty("class", "text-primary text-lg")
        phone = QLabel(str(contact.phones[0]))
        phone.setProperty("class", "text-secondary")
        layout.addWidget(label)
        layout.addWidget(phone)
        self.setLayout(layout)