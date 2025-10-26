from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedLayout
from contacts.book import AddressBook
from contacts.records import Record
from serialization import save_data
from widgets.book_summary import BookSummary
from widgets.contact_details import ContactDetails
from widgets.contact_list_wrapper import ContactListWrapper
from widgets.dialogs import AddDialog


class BookWidget(QWidget):
    def __init__(self, book: AddressBook, filename: str):
        super().__init__()

        self.book = book
        self.filename = filename
        self.dialog = None

        # Main area
        self.main = QWidget()
        self.span = QHBoxLayout(self.main)
        self.list = ContactListWrapper(book)
        self.list.setMaximumWidth(240)
        self.list.contactSelected.connect(self.__onContactSelected)
        self.list.addClicked.connect(self.__onAdd)
        self.details = BookSummary(book)
        self.span.addWidget(self.list)
        self.span.addWidget(self.details)

        # Dialog overlay
        self.overlay = QWidget()
        self.overlay.setProperty("class", "overlay")
        self.overlay_layout = QVBoxLayout(self.overlay)

        self.stack = QStackedLayout(self)
        self.stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.stack.addWidget(self.overlay)
        self.stack.addWidget(self.main)
        self.overlay.hide()  # Start hidden


    @Slot()
    def __onContactSelected(self, contact: Record | None):
        if contact:
            self.setUpdatesEnabled(False)
            self.span.removeWidget(self.details)
            self.details.deleteLater()
            self.details = ContactDetails(contact)
            self.details.editClicked.connect(self.__onEdit)
            self.details.deleteClicked.connect(self.__onDelete)
            self.span.addWidget(self.details)
            self.setUpdatesEnabled(True)

    @Slot()
    def __onAdd(self):
        if self.dialog:
            return
        
        def save(name: str, phone: str):
            contact = Record(name)
            contact.add_phone(phone)
            self.book.add_record(contact)
            self.list.add_record(contact)
            save_data(self.book, self.filename)
            self.close_dialog()
        
        self.dialog = AddDialog()
        self.dialog.closeClicked.connect(self.close_dialog)
        self.dialog.saveClicked.connect(save)
        self.overlay_layout.addWidget(self.dialog, alignment=Qt.AlignmentFlag.AlignCenter)
        self.overlay.show()

    @Slot()
    def __onDelete(self, contact: Record):
        self.book.delete(contact.name.value)
        self.list.delete_record(contact)
        save_data(self.book, self.filename)

    @Slot()
    def __onEdit(self, contact: Record):
        if self.dialog:
            return
        
        self.dialog = AddDialog(contact.name.value, contact.phones[0].value)
        self.dialog.closeClicked.connect(self.close_dialog)
        self.overlay_layout.addWidget(self.dialog, alignment=Qt.AlignmentFlag.AlignCenter)
        self.overlay.show()

    def close_dialog(self):
        self.overlay.hide()
        if self.dialog:
            self.overlay_layout.removeWidget(self.dialog)
            self.dialog.deleteLater()
            self.dialog = None
