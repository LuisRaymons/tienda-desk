from PyQt5.QtGui import QIcon,QFont
from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view.Errors import ErrorGeneral
from controller import PromotorController

from config import env
import cv2
import os
import imutils
import numpy as np
from PIL import Image


class PromotorView:
    def __init__(self):
        self.ctrpromotor = PromotorController.PromotorController()
        self.msm = ErrorGeneral.ErrorGeneral()
        self.rutaimg = ""
        self.rutaimgedit = ""
    def getpromotores(self,token,pagina,registropagina):
        datatable = self.ctrpromotor.getpromotores(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data;

        for i,d in enumerate(self.dataRefresh):
            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(d['nombre']))
            self.tableRefresh.setItem(i, 2, QTableWidgetItem(d['direccion']))
            self.tableRefresh.setItem(i, 3, QTableWidgetItem(d['telefono']))
            self.tableRefresh.setItem(i, 4, QTableWidgetItem(d['sitioWeb']))
            self.tableRefresh.setItem(i, 5, QTableWidgetItem(QtGui.QIcon(QtGui.QPixmap(d['img'])),d['img'],1))
    def createview(self,token,tab):
        labelnombre = QLabel("Nombre: ",tab)
        labelnombre.setGeometry(30,30,100,30)

        self.txtnombre = QLineEdit(tab)
        self.txtnombre.setGeometry(90,30,400,30)

        labeldireccion = QLabel("Direccion: ", tab)
        labeldireccion.setGeometry(30,80,100,30)

        self.txtdireccion = QLineEdit(tab)
        self.txtdireccion.setGeometry(90,80,400,30)

        labeltelefono = QLabel("Telefono: ", tab)
        labeltelefono.setGeometry(30,130,100,30)

        self.txttelefono = QLineEdit(tab)
        self.txttelefono.setGeometry(90,130,400,30)

        labelwebsite = QLabel("Citio web: ", tab)
        labelwebsite.setGeometry(30,180,100,30)

        self.txtwebsite = QLineEdit(tab)
        self.txtwebsite.setGeometry(90,180,400,30)

        labelimg = QLabel("Imagen: ", tab)
        labelimg.setGeometry(30,230,100,30)

        buttonimg = QPushButton(tab)
        buttonimg.setGeometry(90,230,400,30)
        buttonimg.setIcon(QIcon('icon/seleccione.png'))
        buttonimg.setText("Seleccione Foto")
        buttonimg.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimg.clicked.connect(lambda: self.fieldselected(1))

        buttonsaveproveedor = QPushButton(tab)
        buttonsaveproveedor.setGeometry(30,270,400,30)
        buttonsaveproveedor.setText("Guardar")
        buttonsaveproveedor.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsaveproveedor.clicked.connect(lambda: self.saveproveedor(token))

        self.img = QLabel(tab)
        self.img.setGeometry(700,30,400,400)
    def fieldselected(self,type):
        self.fileFrame = QDialog()
        self.fileFrame.setWindowTitle("Archivo para imagen")
        self.fileFrame.setFixedSize(320, 200)
        self.openFileNameDialog(type)
    def openFileNameDialog(self,type):

        options = QFileDialog.Options()
        ##options |= QFileDialog.DontUseNativeDialog
        filename, __ = QFileDialog.getOpenFileName(self.fileFrame,"Seleccione una imagen del producto", "","All Files (*);;PNG,JPG,JPEG Image(*.png,*.jpg,*.jpeg)", options=options)

        if filename:

            file = filename.split('/')
            namefile = file[len(file) - 1]
            namefull = namefile.replace(" ","-")

            imagen = cv2.imread(filename)

            if not os.path.exists(env.IPRESOURCEIMG +'/promotor/'):
                os.makedirs(env.IPRESOURCEIMG +'/promotor/')
            cv2.imwrite(env.IPRESOURCEIMG +'/promotor/' + namefull, imagen)

            ## ruta img  self.rutaimgedit

            if(type == 1):
                self.rutaimg = str(env.IPRESOURCEIMG +'/promotor/') + namefull
                saveImgProduct = QtGui.QPixmap(filename)
                imgProduct = saveImgProduct.scaled(240,240)
                self.img.setPixmap(imgProduct)
            elif(type == 2):
                self.rutaimgedit = str(env.IPRESOURCEIMG +'/promotor/') + namefull
                saveImgProduct = QtGui.QPixmap(filename)
                imgProduct = saveImgProduct.scaled(240,240)
                self.imgedit.setPixmap(imgProduct)
    def saveproveedor(self,token):
        if(self.txtnombre.text() == ''):
            self.msm.messageInfo("Campo requerido","El nombre del promotor es requerido")
        elif(self.txtdireccion.text() == ''):
            self.msm.messageInfo("Campo requerido","La direccion del promotor es requerido")
        elif(self.txttelefono.text() == ''):
            self.msm.messageInfo("Campo requerido","El telefono del promotor es requerido")
        else:
            args = {"api_token":token,"name":self.txtnombre.text(),"address":self.txtdireccion.text(),"phone":self.txttelefono.text(),"website":self.txtwebsite.text()}

            if(self.rutaimg == ''):
                files = {}
            else:
                files = {'img': open(self.rutaimg,'rb')}

            guardar = self.msm.messageConfirm("Guardar Promotor","¿Quieres guardar al promotor?")

            if(guardar == True):
                promotor = self.ctrpromotor.store(args,files)
                if(promotor['code'] == 200):
                    self.tableRefresh.clearContents()
                    datos = self.getpromotores(token,1,20)
                    self.table(self.tableRefresh,datos['data'])
                    self.limiparinput()
                self.msm.messageInfo("Usuario " + promotor['status'], promotor['msm']);
    def limiparinput(self):
        self.txtnombre.clear()
        self.txtdireccion.clear()
        self.txttelefono.clear()
        self.txtwebsite.clear()
    def edit(self,token,data):
        self.frameedit = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.frameedit.setWindowModality(Qt.ApplicationModal)
        self.frameedit.setWindowTitle("Modificar al promotor " + data[1])
        self.frameedit.setWindowIcon(QIcon('icon/tienda.png'))
        self.frameedit.setFixedSize(800, 350)

        self.ideditpromotor = data[0]

        labelnombreedit = QLabel("Nombre: ",self.frameedit)
        labelnombreedit.setGeometry(30,30,100,30)

        self.txtnombreedit = QLineEdit(self.frameedit)
        self.txtnombreedit.setText(data[1])
        self.txtnombreedit.setGeometry(90,30,400,30)

        labeldireccionedit = QLabel("Direccion: ", self.frameedit)
        labeldireccionedit.setGeometry(30,80,100,30)

        self.txtdireccionedit = QLineEdit(self.frameedit)
        self.txtdireccionedit.setText(data[2])
        self.txtdireccionedit.setGeometry(90,80,400,30)

        labeltelefonoedit = QLabel("Telefono: ", self.frameedit)
        labeltelefonoedit.setGeometry(30,130,100,30)

        self.txttelefonoedit = QLineEdit(self.frameedit)
        self.txttelefonoedit.setText(data[3])
        self.txttelefonoedit.setGeometry(90,130,400,30)

        labelwebsiteedit = QLabel("Citio web: ", self.frameedit)
        labelwebsiteedit.setGeometry(30,180,100,30)

        self.txtwebsiteedit = QLineEdit(self.frameedit)
        self.txtwebsiteedit.setText(data[4])
        self.txtwebsiteedit.setGeometry(90,180,400,30)

        labelimgedit = QLabel("Imagen: ", self.frameedit)
        labelimgedit.setGeometry(30,230,100,30)

        buttonimg = QPushButton(self.frameedit)
        buttonimg.setGeometry(90,230,400,30)
        buttonimg.setIcon(QIcon('icon/seleccione.png'))
        buttonimg.setText("Seleccione Foto")
        buttonimg.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimg.clicked.connect(lambda: self.fieldselected(2))

        buttonsaveproveedor = QPushButton(self.frameedit)
        buttonsaveproveedor.setGeometry(30,270,460,30)
        buttonsaveproveedor.setText("Guardar")
        buttonsaveproveedor.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsaveproveedor.clicked.connect(lambda: self.saveupdateproveedor(token))

        self.imgedit = QLabel(self.frameedit)
        self.imgedit.setGeometry(520,0,300,300)

        self.frameedit.exec_()
    def saveupdateproveedor(self,token):

        if(self.txtnombreedit.text() == ''):
            self.msm.messageInfo("Campo requerido","El nombre del promotor es requerido")
        elif(self.txtdireccionedit.text() == ''):
            self.msm.messageInfo("Campo requerido","La direccion del promotor es requerido")
        elif(self.txttelefonoedit.text() == ''):
            self.msm.messageInfo("Campo requerido","El telefono del promotor es requerido")
        else:
            args = {"api_token":token, "id":self.ideditpromotor,"name":self.txtnombreedit.text(),"address":self.txtdireccionedit.text(),"phone":self.txttelefonoedit.text(),"website":self.txtwebsiteedit.text()}
            print(args)
            print("-----------------------------")

            if(self.rutaimgedit == ''):
                files = {}
            else:
                files = {'img': open(self.rutaimgedit,'rb')}

            guardar = self.msm.messageConfirm("Guardar Promotor","¿Quieres guardar al promotor?")

            if(guardar == True):
                promotorupdate = self.ctrpromotor.update(args,files)
                if(promotorupdate['code'] == 200):
                    self.tableRefresh.clearContents()
                    datos = self.getpromotores(token,1,20)
                    self.table(self.tableRefresh,datos['data'])
                    self.frameedit.close()
                self.msm.messageInfo("Usuario " + promotorupdate['status'], promotorupdate['msm']);

    def delete(self,token,data):
        confirm = self.msm.messageConfirm("Confirmar eliminar a " + data[1],"¿Quieres continuar con la eliminacion del promotor?")

        if(confirm):
            promotor = self.ctrpromotor.delete(token,data[0])
            if(promotor['code'] == 200):
                self.msm.messageInfo("Promotor " + promotor['status'],promotor['msm'])
                self.tableRefresh.clearContents()
                datos = self.getpromotores(token,1,20)
                self.table(self.tableRefresh,datos['data'])
