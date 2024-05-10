from UI_main_window import Ui_Dialog
from frameless_window import FramelessWindow
import sys
from PyQt6 import QtWidgets, uic
import pygetwindow
import pyautogui
import ocr_translation_functions
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from numpy import ndarray


class MainWindow(QtWidgets.QMainWindow):
    translation_request = Signal(ndarray)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  
        self.ui.windowComboBox.addItems(pygetwindow.getAllTitles())
        self.overlay = FramelessWindow()

        self.worker = OCRTranslationWorker()
        self.worker_thread = QThread()

        self.ui.translateButton.pressed.connect(self.start)
        self.worker.translation_completed.connect(self.complete)
        self.translation_request.connect(self.worker.translate_window)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
    """
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
    """
    
    def start(self):
        self.overlay.hide()
        window_title = self.ui.windowComboBox.currentText()
        game_frame = ocr_translation_functions.get_window_capture(window_title=window_title)
        self.translation_request.emit(game_frame)
        self.overlay.show()

    def complete(self, results):
        window_title = self.ui.windowComboBox.currentText()
        window = pygetwindow.getWindowsWithTitle(window_title)[0]
        self.overlay = FramelessWindow(is_frameless=True, top_pos=window.top, left_pos=window.left, width=window.width, height=window.height)
        self.overlay.load_image(results['img'])
        self.overlay.show()
        print(results['texts'])



class OCRTranslationWorker(QObject):
    translation_completed = Signal(dict)

    @Slot(ndarray)
    def translate_window(self, window_capture: ndarray):
        scan_results = ocr_translation_functions.get_results_from_capture(window_capture)
        self.translation_completed.emit(scan_results)

