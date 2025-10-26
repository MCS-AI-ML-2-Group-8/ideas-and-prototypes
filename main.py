import sys
import cli
from pathlib import Path
from PySide6.QtWidgets import QApplication
from serialization import load_data
from widgets.book_widget import BookWidget

def main():
    filename = "./data/addressbook.pkl"
    
    if "--ui" in sys.argv:
        book = load_data(filename)
        app = QApplication([])
        app.setStyleSheet(Path("./styles/styles.qss").read_text())
        widget = BookWidget(book, filename)
        widget.resize(800, 600)
        widget.show()
        app.exec()
    else:
        cli.launch_main_loop(filename)

if __name__ == "__main__":
    main()