from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt as tr
from PyQt5.QtGui import QIcon,QFont
from os import remove, path
from view.Errors import ErrorGeneral as msmview

import sys
import math
import threading

class HomeView(QtWidgets.QMainWindow):

    def __init__(self, data, loginview):
        self.data = data
        self.loginview = loginview
        self.msm = msmview.ErrorGeneral()
        super(HomeView, self).__init__()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 801, 601))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, -10, 201, 611))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.frame_2)
        self.treeWidget.setGeometry(QtCore.QRect(0, -15, 201, 900))
        self.treeWidget.setStyleSheet("background-color: rgb(0, 0, 0) color: rgb(255, 255, 255);")
        self.treeWidget.setObjectName("treeWidget")
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.treeWidget.headerItem().setForeground(0, brush)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("treeviewIcon/product-management.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("treeviewIcon/cateproduct.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon1)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("treeviewIcon/client.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon2)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("treeviewIcon/user.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon3)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("treeviewIcon/product.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon4)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("treeviewIcon/almacen.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon5)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("treeviewIcon/promotore.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon6)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("treeviewIcon/compra.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon7)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("treeviewIcon/venta.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon8)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("treeviewIcon/recurso.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon9)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(200, 0, 601, 591))
        self.frame_3.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Navigation"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Dashboard"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "Categoria Producto"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("MainWindow", "Cliente"))
        self.treeWidget.topLevelItem(3).setText(0, _translate("MainWindow", "Usuario"))
        self.treeWidget.topLevelItem(4).setText(0, _translate("MainWindow", "Producto"))
        self.treeWidget.topLevelItem(5).setText(0, _translate("MainWindow", "Almacen"))
        self.treeWidget.topLevelItem(6).setText(0, _translate("MainWindow", "Promotor"))
        self.treeWidget.topLevelItem(7).setText(0, _translate("MainWindow", "Compra"))
        self.treeWidget.topLevelItem(8).setText(0, _translate("MainWindow", "Venta"))
        self.treeWidget.topLevelItem(9).setText(0, _translate("MainWindow", "Recursos"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)