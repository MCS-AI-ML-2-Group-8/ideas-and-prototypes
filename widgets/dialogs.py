from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton

class BaseDialog(QWidget):

    def __init__(self):
        super().__init__()
        content = QWidget()
        content.setMinimumWidth(600)
        content.setMinimumHeight(450)
        content.setProperty("class", "dialog")
        wrapper = QVBoxLayout(self)
        wrapper.addWidget(content)
        self.content = content


class AddDialog(BaseDialog):
    closeClicked = Signal()
    saveClicked = Signal(str, str)

    def __init__(self, contact_name: str | None = None, phone_number: str | None = None):
        super().__init__()

        contact_name_edit = QLineEdit(contact_name)
        phone_number_edit = QLineEdit(phone_number)

        form = QWidget()
        form_layout = QFormLayout(form)
        form_layout.addRow(self.__createLabel("Name"))
        form_layout.addRow(contact_name_edit)
        form_layout.addRow(self.__createLabel("Phone number"))
        form_layout.addRow(phone_number_edit)
        form_layout.setContentsMargins(50, 50, 50, 50)

        close = QPushButton("Close")
        close.setFixedSize(120, 40)
        close.setProperty("variant", "secondary")
        close.clicked.connect(self.closeClicked)

        save = QPushButton("Save")
        save.setFixedSize(120, 40)
        save.clicked.connect(lambda: self.saveClicked.emit(
            contact_name_edit.text(),
            phone_number_edit.text()))

        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.addWidget(close)
        buttons_layout.addWidget(save)

        layout = QVBoxLayout(self.content)
        layout.addWidget(form)
        layout.addStretch()
        layout.addWidget(buttons, alignment=Qt.AlignmentFlag.AlignCenter)

    def __createLabel(self, text: str):
        label = QLabel(text)
        label.setProperty("variant", "form")
        return label
