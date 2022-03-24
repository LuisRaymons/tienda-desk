from slugify import slugify
from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from controller import LoginController
from view import HomeView
from view.Errors import ErrorGeneral
#from moduloFace import CapturaRostro
from config import env as config
import sys
import requests
import json

class LoginView(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginView, self).__init__()
        self.LC=LoginController.LoginController()
        self.msm = ErrorGeneral.ErrorGeneral()
    def viewLogin(self):
        app = QApplication(sys.argv)
        self.LoginShowView = QWidget(None, QtCore.Qt.WindowCloseButtonHint)

        self.LoginShowView.setWindowTitle('Login LRVA')
        self.LoginShowView.setWindowIcon(QIcon('icon/tienda.png'))
        self.LoginShowView.setGeometry(450,320,450,230)

        self.tabWidget = QtWidgets.QTabWidget(self.LoginShowView)
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1265, 700))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Login"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Register"))

        login = self.loginvista(self.tab)
        register = self.loginregister(self.tab_2)

        self.LoginShowView.show()
        sys.exit(app.exec_())
    def loginvista(self,tab):

        label_correo = QLabel("Correo: ",tab)
        label_correo.setGeometry(10,10,70,40)

        txt_correo = QLineEdit(tab)
        txt_correo.setPlaceholderText('Correo electronico')
        txt_correo.setGeometry(80,10,360,25)
        txt_correo.setFocus()

        label_password = QLabel("Contraseña: ", tab)
        label_password.setGeometry(10,50,70,40)

        passwordtxt = QLineEdit(tab)
        passwordtxt.setPlaceholderText('Contraseña de accesso')
        passwordtxt.setEchoMode(QLineEdit.Password)
        passwordtxt.setGeometry(80,50,360,25)

        button_login = QPushButton(tab)
        button_login.setText("Entrar")
        button_login.clicked.connect(lambda: self.loginApi(txt_correo.text(),passwordtxt.text()))
        button_login.setGeometry(10,90,430,30)
        button_login.setStyleSheet("background-color: #13AA28;")

        #button_face = QPushButton(tab)
        #button_face.setText("Reconocer face")
        #button_face.clicked.connect(lambda: self.faceCapt.reconocimiento(self.LoginShowView))
        #button_face.setGeometry(10,130,430,30)
        #button_face.setStyleSheet("background-color: #4075CC;")
    def loginregister(self, tab):
        labelnombre = QLabel("*Nombre: ", tab)
        labelnombre.setGeometry(10,10,50,25)

        self.nombretxt = QLineEdit(tab)
        self.nombretxt.setGeometry(80,10,350,25)

        labelcorreo = QLabel("*Correo: ", tab)
        labelcorreo.setGeometry(10,40,60,25)

        self.correotxt = QLineEdit(tab)
        self.correotxt.setGeometry(80,40,350,25)

        labelpassword = QLabel("*Password: ", tab)
        labelpassword.setGeometry(10,70,60,25)

        self.passwordtxt =QLineEdit(tab)
        self.passwordtxt.setGeometry(80,70,350,25)

        labelconfirmpassword = QLabel("*Confirmar password: ", tab)
        labelconfirmpassword.setGeometry(10,100,110,25)

        self.confirmpasswordtxt = QLineEdit(tab)
        self.confirmpasswordtxt.setGeometry(130,100,300,25)

        btnguardar = QPushButton(tab)
        btnguardar.setText("Guardar")
        btnguardar.setGeometry(10,130,420,30)
        btnguardar.clicked.connect(lambda: self.store())
        btnguardar.setStyleSheet("background-color: #13AA28;")
    def loginApi(self,correo,password):

        correo2 = slugify(correo, separator=" ", regex_pattern = r'[^-a-z0-9_@.]+')
        correo3 = correo2.replace(" ", "")
        if "@" in correo3:
            self.login = self.LC.auth(correo3,password)

            if(self.login['code'] == 200):

                if(self.login['data']['type'] in('Administrador','Vendedor')):
                    self.LoginShowView.close()
                    self.paginaPrincipal = HomeView.HomeView(self.login['data'],self.LoginShowView)
                    self.paginaPrincipal.show()
                else:
                    self.msm.messageError("credenciales incorrectas","Las credenciales ingresadas son incorrecta, intente nuavamente")
                    self.LoginShowView.show()
            else:
                self.msm.messageError("credenciales incorrectas","Las credenciales ingresadas son incorrecta, intente nuavamente")
        else:
            self.msm.messageError("Correo Incorrecto", "El correo ingresado no es valido, ejemplo(correo@example.com)")
    def store(self):
        nombre = self.nombretxt.text()
        correo = self.correotxt.text()
        password = self.passwordtxt.text()
        confirmpassword = self.confirmpasswordtxt.text()

        if(nombre == ''):
            self.msm.messageError("Campo requerido","El nombre del usuario es requerido")
        elif(correo == ''):
            self.msm.messageError("Campo requerido","El correo electronico es requerido")
        else:
            if(password != confirmpassword):
                self.msm.messageError("Contraseñas no cohiciden", "Las contraseñas no cohiciden")
            elif("@" not in correo):
                self.msm.messageError("El correo invalido", "El correo introduccido no tiene formato correcto ejem. (elcorreo@hotmail.com.mx)")
            else:
                args = {"api_token":'MqN7lCKFy0lRfXxnhjYLnVf5Pkg83K',"name":nombre,"email":correo,
                        "password":password,"confirmpassword":confirmpassword,"typeuser":'Vendedor'}

                files = {}

                guardar = self.msm.messageConfirm("Registrar usuario","¿Quieres guardar al usuario?")
                if(guardar == True):
                    usercreate = self.LC.store(args)
                    if(usercreate['code'] == 200):
                        # Entrar a la pantalla principal y abtes darle un mensaje de bienvenida al usuario registrado
                        self.LoginShowView.close()
                        self.paginaPrincipal = HomeView.HomeView(usercreate['data'],self.LoginShowView)
                        self.paginaPrincipal.show()

                    self.msm.messageInfo("Usuario " + usercreate['status'], usercreate['msm']);
