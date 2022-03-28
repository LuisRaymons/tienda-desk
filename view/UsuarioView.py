from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view.Errors import ErrorGeneral
from controller import UsuarioController
from config import env
import cv2
import os
import imutils
import numpy as np
from PIL import Image

class UsuarioView:
    def __init__(self):
        self.ctrusuario = UsuarioController.UsuarioController()
        self.msm = ErrorGeneral.ErrorGeneral()
        self.rutaimg = ""
        self.rutaimgedit = ""
    def getusurios(self,token,pagina,registropagina):
        datatable = self.ctrusuario.getusurios(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data;

        for i,d in enumerate(self.dataRefresh):
            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(d['name']))
            self.tableRefresh.setItem(i, 2, QTableWidgetItem(d['email']))
            self.tableRefresh.setItem(i, 3, QTableWidgetItem(d['type']))
            self.tableRefresh.setItem(i, 4, QTableWidgetItem(QtGui.QIcon(QtGui.QPixmap(env.URLRESOURCE + str(d['img']))),env.URLRESOURCE + str(d['img']),1))
    def createview(self,token,tab):
        labelnombre = QLabel("Nombre:", tab)
        labelnombre.setGeometry(30,30,110,30)

        self.txtnombre = QLineEdit(tab)
        self.txtnombre.setGeometry(150,30,400,30)

        labelemail = QLabel("Correo: ",tab)
        labelemail.setGeometry(30,80,110,30)

        self.txtemail = QLineEdit(tab)
        self.txtemail.setGeometry(150,80,400,30)

        labelpassword = QLabel("Contreseña: ", tab)
        labelpassword.setGeometry(30,130,110,30)

        self.txtpassword = QLineEdit(tab)
        self.txtpassword.setGeometry(150,130,400,30)

        labelconfirmapassword = QLabel("Confirmar contraseña: ", tab)
        labelconfirmapassword.setGeometry(30,180,110,30)

        self.txtconfirmpass = QLineEdit(tab)
        self.txtconfirmpass.setGeometry(150,180,400,30)

        labeltype = QLabel("Tipo usuario: ", tab)
        labeltype.setGeometry(30,230,110,30)

        self.txttype = QComboBox(tab)
        self.txttype.addItem("Selecciona el tipo de usuario")
        self.txttype.addItem("Cliente")
        self.txttype.addItem("Vendedor")
        self.txttype.addItem("Administrador")
        self.txttype.setGeometry(150,230,400,30)

        labelimg = QLabel("Imagen: ", tab)
        labelimg.setGeometry(30,280,110,30)

        buttonimg = QPushButton(tab)
        buttonimg.setGeometry(100,280,450,30)
        buttonimg.setIcon(QIcon('icon/seleccione.png'))
        buttonimg.setText("Seleccione Foto")
        buttonimg.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimg.clicked.connect(lambda: self.fieldselected(1))

        buttonsabeclient = QPushButton(tab)
        buttonsabeclient.setGeometry(30,330,520,30)
        buttonsabeclient.setText("Guardar")
        buttonsabeclient.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsabeclient.clicked.connect(lambda: self.saveuser(token))

        self.img = QLabel(tab)
        self.img.setGeometry(700,30,400,400)
    def fieldselected(self,type):
        self.fileFrame = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.fileFrame.setWindowTitle("Archivo para imagen")
        self.fileFrame.setFixedSize(320, 200)
        self.openFileNameDialog(type)
    def openFileNameDialog(self,type):

        options = QFileDialog.Options()
        self.rutaimg, __ = QFileDialog.getOpenFileName(self.fileFrame,"Seleccione una imagen del producto", "","All Files (*);;PNG,JPG,JPEG Image(*.png,*.jpg,*.jpeg)", options=options)

        if self.rutaimg:
            saveImgUser = QPixmap(self.rutaimg)
            imguser = saveImgUser.scaled(240,240)

            if(type == 1):
                self.img.setPixmap(imguser) # ver imagen en create cliente
            elif(type == 2):
                self.imgedit.setPixmap(imguser)
    def saveuser(self,token):
        if(self.txtnombre.text() == ''):
            self.msm.messageError("Campo requerido","El nombre del usuario es requerido")
        elif(self.txtemail.text() == ''):
            self.msm.messageError("Campo requerido","El correo electronico es requerido")
        elif(self.txtpassword.text() == ''):
            self.msm.messageError("Campo requerido","La contraseña es requerida")
        elif(self.txtconfirmpass.text() == ''):
            self.msm.messageError("Campo requerido", "Necesitas confirmar tu contraseña")
        else:
            if(self.txtpassword.text() != self.txtconfirmpass.text()):
                self.msm.messageError("Contraseñas no cohiciden", "Las contraseñas no cohiciden")
            elif( "@" not in self.txtemail.text()):
                self.msm.messageError("El correo invalido", "El correo introduccido no tiene formato correcto ejem. (elcorreo@hotmail.com.mx)")
            else:
                typeuser = "Cliente" if self.txttype.currentText() == "Selecciona el tipo de usuario" else self.txttype.currentText()
                args = {"api_token":token,"name":self.txtnombre.text(),"email":self.txtemail.text(),"password":self.txtpassword.text(),"confirmpassword":self.txtconfirmpass.text(),"typeuser":self.txttype.currentText()}

                if(self.rutaimg == ''):
                    files = {}
                else:
                    files = {'img': open(self.rutaimg,'rb')}

                guardar = self.msm.messageConfirm("Guardar usuario","¿Quieres guardar al usuario?")
                if(guardar == True):
                    user = self.ctrusuario.store(args,files)
                    if(user['code'] == 200):
                        self.limpiarinput()
                        self.tableRefresh.clearContents()
                        datos = self.getusurios(token,1,20)
                        self.table(self.tableRefresh,datos['data'])
                    self.msm.messageInfo("Usuario " + user['status'], user['msm'])
    def limpiarinput(self):
        self.txtnombre.clear()
        self.txtemail.clear()
        self.txtpassword.clear()
        self.txtconfirmpass.clear()
        self.txttype.clear()
        self.txttype.addItem("Selecciona el tipo de usuario")
        self.txttype.addItem("Cliente")
        self.txttype.addItem("Vendedor")
        self.txttype.addItem("Administrador")
        self.img.clear()
        self.rutaimg = ""
    def edit(self,token,data):

        self.frameupdate = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.frameupdate.setWindowModality(Qt.ApplicationModal)
        self.frameupdate.setWindowTitle("Modificar al usuario " + data[1])
        self.frameupdate.setWindowIcon(QIcon('icon/tienda.png'))
        self.frameupdate.setFixedSize(850, 500)

        self.idedit = data[0]
        labelnombreedit = QLabel("Nombre:", self.frameupdate)
        labelnombreedit.setGeometry(30,30,110,30)

        self.txtnombreedit = QLineEdit(self.frameupdate)
        self.txtnombreedit.setGeometry(150,30,400,30)
        self.txtnombreedit.setText(data[1])

        labelemailedit = QLabel("Correo: ",self.frameupdate)
        labelemailedit.setGeometry(30,80,110,30)

        self.txtemailedit = QLineEdit(self.frameupdate)
        self.txtemailedit.setGeometry(150,80,400,30)
        self.txtemailedit.setText(data[2])

        self.changepass = QCheckBox(" Cambiar contraseña", self.frameupdate)
        self.changepass.move(20,20)
        self.changepass.resize(320,40)
        self.changepass.setGeometry(150,130,170,30)
        self.changepass.stateChanged.connect(self.changepassword)

        self.labelpassword = QLabel("Contreseña: ", self.frameupdate)
        self.labelpassword.setVisible(False)
        self.labelpassword.setGeometry(30,180,110,30)

        self.txtpasswordedit = QLineEdit(self.frameupdate)
        self.txtpasswordedit.setVisible(False)
        self.txtpasswordedit.setGeometry(150,180,400,30)

        self.labelconfirmapassword = QLabel("Confirmar contraseña: ", self.frameupdate)
        self.labelconfirmapassword.setVisible(False)
        self.labelconfirmapassword.setGeometry(30,230,110,30)

        self.txtconfirmpassedit = QLineEdit(self.frameupdate)
        self.txtconfirmpassedit.setVisible(False)
        self.txtconfirmpassedit.setGeometry(150,230,400,30)

        labeltype = QLabel("Tipo usuario: ", self.frameupdate)
        labeltype.setGeometry(30,280,110,30)

        self.txttypeedit = QComboBox(self.frameupdate)
        self.txttypeedit.addItem("Selecciona el tipo de usuario")
        self.txttypeedit.addItem("Cliente")
        self.txttypeedit.addItem("Vendedor")
        self.txttypeedit.addItem("Administrador")
        self.txttypeedit.setGeometry(150,280,400,30)
        indexposition = 0
        for i,typeselect in enumerate(['Selecciona el tipo de usuario','Cliente','Vendedor','Administrador']):
            if(typeselect == data[3]):
                indexposition = i
        self.txttypeedit.setCurrentIndex(indexposition)

        labelimg = QLabel("Imagen: ", self.frameupdate)
        labelimg.setGeometry(30,330,110,30)

        buttonimg = QPushButton(self.frameupdate)
        buttonimg.setGeometry(100,330,450,30)
        buttonimg.setIcon(QIcon('icon/seleccione.png'))
        buttonimg.setText("Seleccione Foto")
        buttonimg.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimg.clicked.connect(lambda: self.fieldselected(2))

        buttonsabeclient = QPushButton(self.frameupdate)
        buttonsabeclient.setGeometry(30,380,520,30)
        buttonsabeclient.setText("Guardar")
        buttonsabeclient.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsabeclient.clicked.connect(lambda: self.saveupdateuser(token))

        self.imgedit = QLabel(self.frameupdate)
        self.imgedit.setGeometry(600,30,400,400)

        self.frameupdate.show()
    def saveupdateuser(self,token):
        if(self.txtnombreedit.text() == ''):
            self.msm.messageError("Campo requerido","El nombre del usuario es requerido")
        elif(self.txtemailedit.text() == ''):
            self.msm.messageError("Campo requerido","El correo electronico es requerido")
        else:
            if(self.txtpasswordedit.text() != self.txtconfirmpassedit.text()):
                self.msm.messageError("Contraseñas no cohiciden", "Las contraseñas no cohiciden")
            elif( "@" not in self.txtemailedit.text()):
                self.msm.messageError("El correo invalido", "El correo introduccido no tiene formato correcto ejem. (elcorreo@hotmail.com.mx)")
            else:
                typeuser = "Cliente" if self.txttypeedit.currentText() == "Selecciona el tipo de usuario" else self.txttypeedit.currentText()
                args = {"api_token":token,"id":self.idedit,"name":self.txtnombreedit.text(),"email":self.txtemailedit.text(),"password":self.txtpasswordedit.text(),"confirmpassword":self.txtconfirmpassedit.text(),"typeuser":self.txttypeedit.currentText()}

                if(self.rutaimg == ''):
                    files = {}
                else:
                    files = {'img': open(self.rutaimg,'rb')}

                guardar = self.msm.messageConfirm("Guardar usuario","¿Quieres Guardar al usuario?")
                if(guardar == True):
                    useredit = self.ctrusuario.update(args,files)
                    if(useredit['code'] == 200):
                        self.frameupdate.close()
                        self.tableRefresh.clearContents()
                        datos = self.getusurios(token,1,20)
                        self.table(self.tableRefresh,datos['data'])
                        self.rutaimg = ""
                    self.msm.messageInfo("Usuario " + useredit['status'], useredit['msm']);
    def changepassword(self,state):
        print(state)

        if(state == 0):
            self.labelpassword.setVisible(False)
            self.txtpasswordedit.setVisible(False)
            self.labelconfirmapassword.setVisible(False)
            self.txtconfirmpassedit.setVisible(False)
        elif(state == 2):
            self.labelpassword.setVisible(True)
            self.txtpasswordedit.setVisible(True)
            self.labelconfirmapassword.setVisible(True)
            self.txtconfirmpassedit.setVisible(True)
    def delete(self,token,data,iduser):
        print(type(data[0]))
        print(type(iduser))

        if(int(data[0]) == iduser):
            self.msm.messageError("Error al eliminar el usuario","El usuario que intentas eliminar eres tu y no te puedes auto eliminar, llama a otro administrador para eliminarte")
        else:
            confirm = self.msm.messageConfirm("Confirmar eliminar a " + data[1],"¿Quieres continuar con la eliminacion de usuario?")
            if(confirm):
                usuario = self.ctrusuario.delete(token,data[0])
                if(usuario['code'] == 200):
                    self.msm.messageInfo("Usuario " + usuario['status'],usuario['msm'])
                    self.tableRefresh.clearContents()
                    datos = self.getusurios(token,1,20)
                    self.table(self.tableRefresh,datos['data'])
