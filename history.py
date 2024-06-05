from PyQt6 import QtCore, QtGui, QtWidgets
from UI_history import Ui_Form

class History(QtWidgets.QDialog):
    def __init__(self, history_dir='./history'):
        super(History, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.history_dir = history_dir
        self.limit = 10
        self.current_position = 0
        self.ui.nextImgBtn.pressed.connect(self.go_to_next)
        self.ui.previousImgBtn.pressed.connect(self.go_to_previous)

        self.ui.idxViewerLabel.setText(f'{self.current_position} / {self.limit}')

        #add no file/incorrect initial file exception
        self.current_files = {'img': f'{self.history_dir}/output_{self.current_position}.png',
                              'text': f'{self.history_dir}/texts_{self.current_position}.txt'}

        self.img_width = self.ui.imageViewerLabel.size().width()
        self.img_height = self.ui.imageViewerLabel.size().height()
        print(self.ui.imageViewerLabel.size())
        print(self.img_width)
        print(self.img_height)
        pixmap = QtGui.QPixmap(self.current_files['img'])
        pixmap = pixmap.scaled(self.img_width, self.img_height)
        self.ui.imageViewerLabel.setPixmap(pixmap)
        with open(self.current_files['text'], 'r+') as fp:
            self.ui.translatedTextsEdit.setPlainText(fp.read())

    def go_to_previous(self):
        self.current_position -= 1
        if self.current_position < 0:
            self.current_position = 0

        self.ui.idxViewerLabel.setText(f'{self.current_position} / {self.limit}')

        self.current_files = {'img': f'{self.history_dir}/output_{self.current_position}.png',
                              'text': f'{self.history_dir}/texts_{self.current_position}.txt'}
        pixmap = QtGui.QPixmap(self.current_files['img'])
        pixmap = pixmap.scaled(self.img_width, self.img_height)
        self.ui.imageViewerLabel.setPixmap(pixmap)
        with open(self.current_files['text'], 'r+') as fp:
            self.ui.translatedTextsEdit.setPlainText(fp.read())

    def go_to_next(self):
        self.current_position += 1
        if self.current_position > self.limit:
            self.current_position = self.limit #limit
        
        self.ui.idxViewerLabel.setText(f'{self.current_position} / {self.limit}')

        self.current_files = {'img': f'{self.history_dir}/output_{self.current_position}.png',
                              'text': f'{self.history_dir}/texts_{self.current_position}.txt'}
        pixmap = QtGui.QPixmap(self.current_files['img'])
        pixmap = pixmap.scaled(self.img_width, self.img_height)
        self.ui.imageViewerLabel.setPixmap(pixmap)
        with open(self.current_files['text'], 'r+') as fp:
            self.ui.translatedTextsEdit.setPlainText(fp.read())
