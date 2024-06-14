import sys
from PyQt6.QtWidgets import QApplication, QSizeGrip, QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor
from PyQt6 import QtWidgets
from PIL import Image
from PIL.ImageQt import ImageQt

class FramelessWindow(QWidget):  
    def __init__(self, is_frameless=True, top_pos=0, left_pos=0, width=100, height=100, parent=None):
        super().__init__(parent=parent)
        self.move(left_pos, top_pos)
        self.setFixedSize(width, height)
        #self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, is_frameless)  # Set frameless flag
        self.setWindowFlag(Qt.WindowType.WindowTransparentForInput, is_frameless)  
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, is_frameless)
        self.setStyleSheet("border : 2px dashed red;") 
        self.setWindowTitle("PyQt Frameless Window")

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, is_frameless)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, is_frameless)  # Set frameless flag

        #self.btn = QPushButton("X", self)
        #self.btn.setGeometry(10, 10, 100, 30)  # Adjust position and size

    def load_image(self, img):
        self.label = QLabel(self)
        
        qim = ImageQt(img)
        pix = QPixmap.fromImage(qim)
 
        # adding image to label
        self.label.setPixmap(pix)
        print(pix.width())
        print(pix.height())
 
        # Optional, resize label to image size
        #window 
        self.setFixedSize(pix.width(), pix.height())
        #image label
        self.label.resize(pix.width(), pix.height())
