from UI_main_window import Ui_Dialog
from frameless_window import FramelessWindow
import sys
from PyQt6 import QtWidgets, uic
import pygetwindow
import pyautogui
import ocr_translation_functions


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  
        self.ui.windowComboBox.addItems(pygetwindow.getAllTitles())
        self.overlay = FramelessWindow()
        self.ui.translateButton.pressed.connect(self.start_translation_current_frame)


    def start_translation_current_frame(self):
        window_title = self.ui.windowComboBox.currentText()
        window = pygetwindow.getWindowsWithTitle(window_title)[0]
        left, top = window.topleft
        game_frame = ocr_translation_functions.get_window_capture(window_title=window_title)
        scan_results = ocr_translation_functions.get_results_from_capture(game_frame)
        self.overlay = FramelessWindow(is_frameless=True, top_pos=top, left_pos=left, width=window.width, height=window.height)
        self.overlay.load_image(scan_results['img'])
        self.overlay.show()
        print(scan_results['texts'])

