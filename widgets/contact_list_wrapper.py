from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from contacts.book import AddressBook
from contacts.records import Record
from .contact_list import ContactList


class ContactListWrapper(QWidget):
    contactSelected = Signal(Record)
    addClicked = Signal()

    def __init__(self, contacts: AddressBook):
        super().__init__()

        self.list = ContactList(contacts.data.values())
        self.list.itemSelectionChanged.connect(self.__onSelectionChanged)

        add_button = QPushButton("Add Contact")
        add_button.setFixedSize(120, 40)
        add_button.clicked.connect(self.addClicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list)
        layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 10)

    def add_record(self, contact: Record):
        self.list.add_record(contact)
    
    def delete_record(self, contact: Record):
        self.list.delete_record(contact)

    @Slot()
    def __onSelectionChanged(self):
        items = self.list.selectedItems()
        if items:
            contact: Record = items[0].data(Qt.ItemDataRole.UserRole)
            self.contactSelected.emit(contact)
        else:
            self.contactSelected.emit(None)
