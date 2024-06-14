from frameless_window import FramelessWindow
from PyQt6.QtWidgets import QApplication
import sys
from main_window import MainWindow
from history import History

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

