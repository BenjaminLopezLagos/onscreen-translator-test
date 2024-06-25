from UI_main_window import Ui_Dialog
from frameless_window import FramelessWindow
from history import History
import sys
from PyQt6 import QtWidgets, uic
import pygetwindow
import pyautogui
from PIL import Image
import ocr_translation_functions
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from numpy import ndarray
import time
import os
import cv2

class MainWindow(QtWidgets.QMainWindow):
    translation_request = Signal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.refresh_window_list()
        self.ui.windowComboBox.setCurrentIndex(0)
        
        self.overlay = FramelessWindow()
        self.history = History()
        self.worker = OCRTranslationWorker()
        self.worker_thread = QThread()

        self.translation_running = False

        self.ui.windowComboBox.currentIndexChanged.connect(self.update_worker_window_title)
        self.ui.updateWindowsButton.pressed.connect(self.refresh_window_list)
        self.ui.historyButton.pressed.connect(self.go_to_history)
        self.ui.translateButton.pressed.connect(self.start_window_translation)
        self.worker.translation_completed.connect(self.complete)
        self.worker.hide_overlay_signal.connect(self.change_overlay_visibility)
        self.translation_request.connect(self.worker.translate_window)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

    def closeEvent(self, event):
        if self.translation_running is True:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "The translation system is still running. Please stop it before exiting.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )
            event.ignore() 

    def start_window_translation(self):
        window_title = self.ui.windowComboBox.currentText()
        self.translation_request.emit(window_title)
        self.ui.translateButton.setText('Pause')
        self.ui.updateWindowsButton.setEnabled(False)

        if self.translation_running is True:
            self.translation_running = False
            self.ui.historyButton.setEnabled(True)
            self.ui.updateWindowsButton.setEnabled(True)
            self.ui.windowComboBox.setEnabled(True)
            self.ui.translateButton.setText('Resume')
            self.worker.stop()
        else:
            self.translation_running = True
            self.translation_request.emit(window_title)
            self.ui.historyButton.setEnabled(False)
            self.ui.updateWindowsButton.setEnabled(False)
            self.ui.windowComboBox.setEnabled(False)
            self.ui.translateButton.setText('Pause')
            self.worker.resume()

    def change_overlay_visibility(self, command):
        if command is True:
            self.overlay.hide()
        else:
            self.overlay.show()

    def complete(self, results):
        window = results['window']
        self.overlay = FramelessWindow(is_frameless=True, top_pos=window.top, left_pos=window.left, width=window.width, height=window.height)
        self.overlay.load_image(results['img'].resize((window.width, window.height), 2))
        self.overlay.show()
        
        os.system('cls')
        print(results['texts'])

        self.ui.translatedTextsEdit.setPlainText('\n'.join('{}) {}'.format(x[0], x[1]) for x in results['texts']).encode("utf-8").decode('cp1252'))

    def go_to_history(self):
        self.history = History()
        self.history.exec()

    def refresh_window_list(self):
        window_list = pygetwindow.getAllTitles()
        window_list = list(filter(None, window_list))
        window_list = list(set(window_list))
        print(window_list)
        self.ui.windowComboBox.clear()
        self.ui.windowComboBox.addItems(window_list)

    def update_worker_window_title(self):
        window_title = self.ui.windowComboBox.currentText()
        self.worker.set_window(window_title)

class OCRTranslationWorker(QObject):
    translation_completed = Signal(dict)
    hide_overlay_signal = Signal(bool)
    translation_data = Signal(dict)
    is_paused = True
    current_window = ''

    @Slot(str)
    def translate_window(self, window_title: str):
        i = 0
        self.current_window = window_title
        previous_results = {'img': '', 'texts': 'empty'}
        while True:
            hide_overlay = True
            self.hide_overlay_signal.emit(hide_overlay)
            try:
                game_frame = ocr_translation_functions.get_window_capture(window_title=self.current_window)
                hide_overlay = False
                self.hide_overlay_signal.emit(hide_overlay)

                if hide_overlay is False:
                    scan_results = ocr_translation_functions.get_results_from_capture(game_frame)
                    scan_results['window'] = pygetwindow.getWindowsWithTitle(self.current_window)[0]
                    self.translation_completed.emit(scan_results)
                    img_w_bouding_box = ocr_translation_functions.get_window_capture(window_title=self.current_window)
                    if scan_results['texts'] and (scan_results['texts'] != previous_results['texts']) and (scan_results['texts'][0][0] != '-'):
                        print('saving img w/ boxes...')
                        Image.fromarray(img_w_bouding_box).save(f'./history/output_{i}.png')
                        with open(f'./history/texts_{i}.txt', 'w') as fp:
                            fp.write('\n'.join('{}) {}'.format(x[0], x[1]) for x in scan_results['texts']))
                            i += 1
                            if i > 9:
                                i = 0
                
                previous_results = scan_results
                
                while self.is_paused is True:
                    hide_overlay = True
                    self.hide_overlay_signal.emit(hide_overlay)  
                    time.sleep(1)
            except Exception as e:
                print('ERROR. Please pause and choose another window.')
                print(e)
                hide_overlay = True
                self.hide_overlay_signal.emit(hide_overlay)  
                break

    def stop(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def set_window(self, new_window):
        self.current_window = new_window