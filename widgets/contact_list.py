from typing import Iterable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from contacts.records import Record
from .contact_list_item import ContactListItem


class ContactList(QListWidget):
    items_by_name: dict[str, QListWidgetItem]

    def __init__(self, contacts: Iterable[Record]):
        super().__init__()
        self.items_by_name = {}
        for contact in contacts:
            self.add_record(contact)

    def add_record(self, contact: Record):
        item = QListWidgetItem()
        element = ContactListItem(contact)
        item.setSizeHint(element.sizeHint())
        item.setData(Qt.ItemDataRole.UserRole, contact)
        self.addItem(item)
        self.setItemWidget(item, element)
        self.items_by_name[contact.name.value] = item

    def delete_record(self, contact: Record):
        item = self.items_by_name.pop(contact.name.value, None)
        if item:
            row = self.row(item)
            self.takeItem(row)