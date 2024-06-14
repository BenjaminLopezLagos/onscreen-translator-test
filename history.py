from PyQt6 import QtCore, QtGui, QtWidgets
from UI_history import Ui_Form
from PIL import Image
from PIL.ImageQt import ImageQt

class History(QtWidgets.QDialog):
    def __init__(self, history_dir='./history'):
        super(History, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.history_dir = history_dir
        self.limit = 10
        self.current_position = 0
        self.images = []
        self.ui.nextImgBtn.pressed.connect(self.go_to_next)
        self.ui.previousImgBtn.pressed.connect(self.go_to_previous)
        self.img_width = self.ui.imageViewerLabel.size().width()
        self.img_height = self.ui.imageViewerLabel.size().height()
        print(self.ui.imageViewerLabel.size())
        print(self.img_width)
        print(self.img_height)

        try:
            self.load_contents()
            print(self.images)
            current_files = self.images[0]
            pixmap = QtGui.QPixmap.fromImage(current_files['img'])
            pixmap = pixmap.scaled(self.img_width, self.img_height)
            self.ui.imageViewerLabel.setPixmap(pixmap)
            self.ui.translatedTextsEdit.setPlainText(current_files['text'])
            self.ui.idxViewerLabel.setText(f'{self.current_position+1} / {self.limit}')
        except:
            print('no files atm')
            self.ui.nextImgBtn.setEnabled(False)
            self.ui.previousImgBtn.setEnabled(False)

    def load_contents(self):
        for i in range(0, self.limit):
            try:
                print(f'{self.history_dir}/output_{i}.png')
                img = Image.open(f'{self.history_dir}/output_{i}.png')
                with open(f'{self.history_dir}/texts_{i}.txt', 'r+') as fp:
                    self.images.append({'img': ImageQt(img),
                                        'text': fp.read()})
            except:
                self.limit = i
                break
                    

    def go_to_previous(self):
        self.current_position -= 1
        if self.current_position < 0:
            self.current_position = 0

        current_files = self.images[self.current_position]
        pixmap = QtGui.QPixmap.fromImage(current_files['img'])
        pixmap = pixmap.scaled(self.img_width, self.img_height)
        self.ui.imageViewerLabel.setPixmap(pixmap)
        self.ui.translatedTextsEdit.setPlainText(current_files['text'])
        self.ui.idxViewerLabel.setText(f'{self.current_position+1} / {self.limit}')

    def go_to_next(self):
        self.current_position += 1
        if self.current_position > self.limit - 1:
            self.current_position = self.limit - 1 # stay on limit
        
        current_files = self.images[self.current_position]
        pixmap = QtGui.QPixmap.fromImage(current_files['img'])
        pixmap = pixmap.scaled(self.img_width, self.img_height)
        self.ui.imageViewerLabel.setPixmap(pixmap)
        self.ui.translatedTextsEdit.setPlainText(current_files['text'])
        self.ui.idxViewerLabel.setText(f'{self.current_position+1} / {self.limit}')
