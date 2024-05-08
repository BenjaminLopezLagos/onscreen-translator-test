from frameless_window import FramelessWindow
from PyQt6.QtWidgets import QApplication
import sys
import pygetwindow
import pyautogui
from main_window import MainWindow
import ocr_translation_functions

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    """
    window_title = 'Spotify Premium'
    window = pygetwindow.getWindowsWithTitle(window_title)[0]
    left, top = window.topleft
    game_frame = ocr_translation_functions.get_window_capture(window_title=window_title)
    scan_results = ocr_translation_functions.get_results_from_capture(game_frame)
    print(scan_results['texts'])

    window2 = FramelessWindow(is_frameless=True, top_pos=top, left_pos=left, width=window.width, height=window.height)
    window2.load_image(scan_results['img'])
    window2.show()
    """
    sys.exit(app.exec())

