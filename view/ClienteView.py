from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon
from view.Errors import ErrorGeneral
from controller import ClienteController
from controller import HomeController
from config import env
import cv2
import os
import imutils
import numpy as np
from PIL import Image

class ClienteView:
    def __init__(self):
        self.ctrCliente = ClienteController.ClienteController();
        self.ctrhome = HomeController.HomeController()
        self.msm = ErrorGeneral.ErrorGeneral()
        self.colonias = []
        self.rutaimg = ""
    def getclientes(self,token,pagina,registropagina):
        datatable = self.ctrCliente.getclientes(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data;

        for i,d in enumerate(self.dataRefresh):
            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(d['nombre']))
            self.tableRefresh.setItem(i, 2, QTableWidgetItem(d['apellidos']))
            self.tableRefresh.setItem(i, 3, QTableWidgetItem(d['telefono']))
            self.tableRefresh.setItem(i, 4, QTableWidgetItem(d['direccion']))
            self.tableRefresh.setItem(i, 5, QTableWidgetItem(str(d['cp'])))
            self.tableRefresh.setItem(i, 6, QTableWidgetItem(d['colonia']))
            """
            imagen = QPixmap(d['img'])
            imgclent = imagen.scaled(80,80)
            self.imgicon = QLabel()
            self.imgicon.setPixmap(imgclent)
            """
            self.tableRefresh.setItem(i, 7, QTableWidgetItem(QtGui.QIcon(QtGui.QPixmap(env.URLRESOURCE + str(d['img']))),env.URLRESOURCE + str(d['img']),1))
            #self.tableRefresh.setCellWidget(i, 7, self.imgicon)
    def createview(self, token,tab):
        labelnombre = QLabel("Nombre: ", tab)
        labelnombre.setGeometry(30,30,100,30)

        self.txtnombre = QLineEdit(tab)
        self.txtnombre.setGeometry(100,30,400,30)

        labelapellidos = QLabel("Apellidos: ", tab)
        labelapellidos.setGeometry(30,80,100,30)

        self.txtlasname = QLineEdit(tab)
        self.txtlasname.setGeometry(100,80,400,30)

        labeltelefono = QLabel("Telefono: ", tab)
        labeltelefono.setGeometry(30,130,100,30)

        self.txttelefono = QLineEdit(tab)
        self.txttelefono.setGeometry(100,130,400,30)

        labeldireccion = QLabel("Direccion: ",tab)
        labeldireccion.setGeometry(30,180,100,30)

        self.txtdireccion = QLineEdit(tab)
        self.txtdireccion.setGeometry(100,180,400,30)

        labelcp = QLabel("Codigo postal: ", tab)
        labelcp.setGeometry(30,230,100,30)

        self.txtcp = QLineEdit(tab)
        self.txtcp.setValidator(QtGui.QIntValidator(1, 99999))
        self.txtcp.setMaxLength(5)
        self.txtcp.textChanged.connect(lambda: self.searchcp(token,1))
        self.txtcp.setGeometry(100,230,400,30)

        labelcolonia = QLabel("Colonia: ", tab)
        labelcolonia.setGeometry(30,280,100,30)

        self.txtcolonia = QComboBox(tab)
        self.txtcolonia.addItem("Seleccione una colonia")
        self.txtcolonia.setGeometry(100,280,400,30)

        labelimg = QLabel("Imagen: ",tab)
        labelimg.setGeometry(30,330,100,30)

        buttonimg = QPushButton(tab)
        buttonimg.setGeometry(100,330,400,30)
        buttonimg.setIcon(QIcon('icon/seleccione.png'))
        buttonimg.setText("Seleccione Foto")
        buttonimg.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimg.clicked.connect(lambda: self.fieldselected(1))

        buttonsabeclient = QPushButton(tab)
        buttonsabeclient.setGeometry(30,380,470,30)
        buttonsabeclient.setText("Guardar")
        buttonsabeclient.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsabeclient.clicked.connect(lambda: self.saveclient(token))

        self.img = QLabel(tab)
        self.img.setGeometry(700,30,400,400)
    def searchcp(self,token,type):

        if(type == 1):
            if(len(self.txtcp.text()) == 5):
                colonias = self.ctrhome.searchcolonias(self.txtcp.text(),token)

                self.txtcolonia.clear()
                self.txtcolonia.addItem("Seleccione una colonia")
                if(colonias['code'] == 200):
                    datos = colonias['data']

                    for col in datos:
                        self.txtcolonia.addItem(col['colonia'])
        elif(type == 2):
            if(len(self.txtcpedit.text()) == 5):
                colonias = self.ctrhome.searchcolonias(self.txtcpedit.text(),token)
                self.selectcoloniaedit.clear()
                self.selectcoloniaedit.addItem("Seleccione una colonia")

                if(colonias['code'] == 200):
                    datos = colonias['data']
                    for col in datos:
                        self.selectcoloniaedit.addItem(col['colonia'])
    def fieldselected(self,type):
        self.fileFrame = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.fileFrame.setWindowTitle("Archivo para imagen")
        self.fileFrame.setFixedSize(320, 200)
        self.openFileNameDialog(type)
    def openFileNameDialog(self,type):

        options = QFileDialog.Options()
        self.rutaimg, __ = QFileDialog.getOpenFileName(self.fileFrame,"Seleccione una imagen del producto", "","All Files (*);;PNG,JPG,JPEG Image(*.png,*.jpg,*.jpeg)", options=options)

        if self.rutaimg:
            saveImgClient = QPixmap(self.rutaimg)
            imgclient = saveImgClient.scaled(240,240)

            if(type == 1):
                self.img.setPixmap(imgclient) # ver imagen en create cliente
            elif(type == 2):
                self.imgedit.setPixmap(imgclient)
    def limpiarinput(self):
        self.txtnombre.clear()
        self.txtlasname.clear()
        self.txttelefono.clear()
        self.txtdireccion.clear()
        self.txtcp.clear()
        self.txtcolonia.clear()
        self.txtcolonia.addItem("Seleccione una colonia")
        self.img.clear()
        self.rutaimg = ""
    def saveclient(self,token):

        if(self.txtnombre.text() == ''):
            self.msm.messageInfo("Campo requerido","El nombre del cliente es requerido")
        elif(self.txtlasname.text() == ''):
            self.msm.messageInfo("Campo requerido","Los apellidos del cliente es requerido")
        elif(self.txttelefono.text() == ''):
            self.msm.messageInfo("Campo requerido", "EL telefono del cliente es requerido")
        elif(self.txtdireccion.text() == ''):
            self.msm.messageInfo("Campo requerido", "La dirreccion del cliente es requerido")
        else:
            print("------------Dato de la imagen status-------------------")
            print(self.rutaimg)
            args = {"api_token":token,"name":self.txtnombre.text(),"lastname":self.txtlasname.text(),"phone":self.txttelefono.text(),"address":self.txtdireccion.text(),"cp":self.txtcp.text(),"colonia":self.txtcolonia.currentText()}

            if(self.rutaimg == ''):
                files = {}
            else:
                files = {'img': open(self.rutaimg,'rb')}

            guardar = self.msm.messageConfirm("Guardar cliente","¿Quieres Guardar al cliente?")

            if(guardar == True):
                cliente = self.ctrCliente.store(args,files)
                if(cliente['code'] == 200):
                    self.limpiarinput()
                self.msm.messageInfo("Cliente " + cliente['status'], cliente['msm']);
    def edit(self,token,data):

        self.frameedit = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.frameedit.setWindowModality(Qt.ApplicationModal)
        self.frameedit.setWindowTitle("Modificar al cliente " + data[1])
        self.frameedit.setWindowIcon(QIcon('icon/tienda.png'))
        self.frameedit.setFixedSize(800, 500)

        self.idclienteupdate = data[0];

        labelnameedit = QLabel("Nombre: ",self.frameedit)
        labelnameedit.setGeometry(30,30,100,30)

        self.txtnombreedit = QLineEdit(self.frameedit)
        self.txtnombreedit.setText(data[1])
        self.txtnombreedit.setGeometry(100,30,400,30)

        labelapellidosedit = QLabel("Apellidos: ", self.frameedit)
        labelapellidosedit.setGeometry(30,80,100,30)

        self.txtapellidoedit = QLineEdit(self.frameedit)
        self.txtapellidoedit.setText(data[2])
        self.txtapellidoedit.setGeometry(100,80,400,30)

        labeltelefonoedit = QLabel("Telefono: ", self.frameedit)
        labeltelefonoedit.setGeometry(30,130,100,30)

        self.txttelefonoedit = QLineEdit(self.frameedit)
        self.txttelefonoedit.setText(data[3])
        self.txttelefonoedit.setGeometry(100,130,400,30)

        labeldireccion = QLabel("Direccion: ", self.frameedit)
        labeldireccion.setGeometry(30,180,100,30)

        self.txtdireccionedit = QLineEdit(self.frameedit)
        self.txtdireccionedit.setText(data[4])
        self.txtdireccionedit.setGeometry(100,180,400,30)

        labelcpedit = QLabel("Codigo Postal: ",self.frameedit)
        labelcpedit.setGeometry(30,230,100,30)

        self.txtcpedit = QLineEdit(self.frameedit)
        self.txtcpedit.setText(data[5])
        self.txtcpedit.setMaxLength(5)
        self.txtcpedit.setValidator(QtGui.QIntValidator(1, 99999))
        self.txtcpedit.textChanged.connect(lambda: self.searchcp(token,2))
        self.txtcpedit.setGeometry(100,230,400,30)

        labelcoloniaedit = QLabel("Colonia: ", self.frameedit)
        labelcoloniaedit.setGeometry(30,280,100,30)

        self.selectcoloniaedit = QComboBox(self.frameedit)
        self.selectcoloniaedit.addItem(data[6])
        self.selectcoloniaedit.addItem("Seleccione una colonia")
        self.selectcoloniaedit.setGeometry(100,280,400,30)

        labelimgedit = QLabel("Imagen: ",self.frameedit)
        labelimgedit.setGeometry(30,330,100,30)

        buttonimgedit = QPushButton(self.frameedit)
        buttonimgedit.setGeometry(100,330,400,30)
        buttonimgedit.setIcon(QIcon('icon/seleccione.png'))
        buttonimgedit.setText("Seleccione Foto")
        buttonimgedit.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimgedit.clicked.connect(lambda: self.fieldselected(2))

        buttonsabeclient = QPushButton(self.frameedit)
        buttonsabeclient.setGeometry(30,380,470,30)
        buttonsabeclient.setText("Guardar")
        buttonsabeclient.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsabeclient.clicked.connect(lambda: self.saveupdateclient(token))

        self.imgedit = QLabel(self.frameedit)
        self.imgedit.setGeometry(550,30,350,350)
        ##self.rutaimgedit = data[7]

        self.frameedit.exec_()
    def saveupdateclient(self,token):

        if(self.txtnombreedit.text() == ''):
            self.msm.messageInfo("Campo requerido","El nombre del cliente es requerido")
        elif(self.txtapellidoedit.text() == ''):
            self.msm.messageInfo("Campo requerido","Los apellidos del cliente es requerido")
        elif(self.txttelefonoedit.text() == ''):
            self.msm.messageInfo("Campo requerido", "EL telefono del cliente es requerido")
        elif(self.txtdireccionedit.text() == ''):
            self.msm.messageInfo("Campo requerido", "La dirreccion del cliente es requerido")
        else:
            args = {"api_token":token,"id":self.idclienteupdate,"name":self.txtnombreedit.text(),"lastname":self.txtapellidoedit.text(),"phone":self.txttelefonoedit.text(),"address":self.txtdireccionedit.text(),
                    "cp":self.txtcpedit.text(),"colonia":self.selectcoloniaedit.currentText()}

            if(self.rutaimg == ''):
                files = {}
            else:
                files = {'img': open(self.rutaimg,'rb')}

            guardar = self.msm.messageConfirm("Guardar cliente","¿Quieres Guardar al cliente?")

            if(guardar == True):

                clienteupdate = self.ctrCliente.update(args,files)

                if(clienteupdate['code'] == 200):
                    self.frameedit.close()
                    self.tableRefresh.clearContents()
                    datos = self.getclientes(token,1,20)
                    self.table(self.tableRefresh,datos['data'])
                    self.rutaimg = ""
                self.msm.messageInfo("Cliente " + clienteupdate['status'], clienteupdate['msm']);
    def delete(self,token,data):

        confirm = self.msm.messageConfirm("Confirmar eliminar a " + data[1],"¿Quieres continuar con la eliminacion del cliente?")

        if(confirm):
            cliente = self.ctrCliente.delete(token,data[0])
            if(cliente['code'] == 200):
                self.msm.messageInfo("Cliente " + cliente['status'],cliente['msm'])
                self.tableRefresh.clearContents()
                datos = self.getclientes(token,1,20)
                self.table(self.tableRefresh,datos['data'])
