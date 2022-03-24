from PyQt5.QtGui import QIcon,QFont,QMovie
from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer


class Loading:
    def __init__(self):
        self.editframe =  QtWidgets.QWidget() #QDialog()
        self.editframe.setWindowTitle("Loading.....")
        self.editframe.setWindowIcon(QIcon('icon/tienda.png'))
        self.editframe.setGeometry(QtCore.QRect(470, 100, 480, 550)) #setFixedSize(192,0,1150, 625)
        self.editframe.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)

        self.labelgif = QLabel(self.editframe)

        self.movie = QMovie("icon/loading.gif")
        self.labelgif.setMovie(self.movie)
        self.labelgif.setGeometry(0,0,490,550)

    def start(self):
        self.editframe.show()
        self.movie.start()

    def stop(self):
        self.movie.stop()
        self.editframe.close()
