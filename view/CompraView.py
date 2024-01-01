from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from view.Errors import ErrorGeneral
from controller import CompraController
from config import env
import string, random
import cv2
import os

class CompraView:
    def __init__(self):
        self.ctrcompra = CompraController.CompraController()
        self.msm = ErrorGeneral.ErrorGeneral()
        self.productos = []
        self.promotores = []
        self.rutaimg = "";
    def getcompras(self,token,pagina,registropagina):
        datatable = self.ctrcompra.getcompras(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data

        for i,d in enumerate(self.dataRefresh):
            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(d['folio']))
            self.tableRefresh.setItem(i, 2, QTableWidgetItem(str(d['cantidad_stock'])))
            self.tableRefresh.setItem(i, 3, QTableWidgetItem(d['precio_total']))
            self.tableRefresh.setItem(i, 4, QTableWidgetItem(QtGui.QIcon(QtGui.QPixmap(d['img'])),d['img'],1))
            self.tableRefresh.setItem(i, 5, QTableWidgetItem(d['promotor']))
            self.tableRefresh.setItem(i, 6, QTableWidgetItem(d['producto']))
    def createview(self,token,tab,userid):
        productos = self.ctrcompra.loadingproducts(token)
        promotores = self.ctrcompra.loadingpromotor(token)
        self.userid = userid
        if(productos['code'] == 200):
            for product in productos['data']:
                self.productos.append(product['nombre'])
        if(promotores['code'] == 200):
            for promotor in promotores['data']:
                self.promotores.append(promotor['nombre'])

        labelcantidad = QLabel("Cantidad: ", tab)
        labelcantidad.setGeometry(30,30,100,30)

        self.txtcantidad = QLineEdit(tab)
        self.txtcantidad.setGeometry(90,30,400,30)
        self.txtcantidad.setMaxLength(10)
        self.txtcantidad.setValidator(QtGui.QIntValidator())

        labelpreciototal = QLabel("Precio total: ", tab)
        labelpreciototal.setGeometry(30,80,100,30)

        self.txtpricetotal = QLineEdit(tab)
        self.txtpricetotal.setGeometry(90,80,400,30)
        self.txtpricetotal.setMaxLength(10)
        self.txtpricetotal.setValidator(QtGui.QDoubleValidator())

        labelimg = QLabel("Ticket: ", tab)
        labelimg.setGeometry(30,130,100,30)

        buttonimg = QPushButton(tab)
        buttonimg.setGeometry(90,130,400,30)
        buttonimg.setIcon(QIcon('icon/seleccione.png'))
        buttonimg.setText("Seleccione Foto")
        buttonimg.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimg.clicked.connect(lambda: self.fieldselected(1))

        labelproducto = QLabel("Producto: ", tab)
        labelproducto.setGeometry(30,180,100,30)

        self.selectproduct = QComboBox(tab)
        self.selectproduct.addItem("Seleccione un producto")
        self.selectproduct.addItems(self.productos)
        self.selectproduct.setGeometry(90,180,400,30)

        labelpromotor = QLabel("Promotor: ", tab)
        labelpromotor.setGeometry(30,230,100,30)

        self.selectpromotor = QComboBox(tab)
        self.selectpromotor.addItem("Seleccione un promotor")
        self.selectpromotor.addItems(self.promotores)
        self.selectpromotor.setGeometry(90,230,400,30)

        buttonsaveproveedor = QPushButton(tab)
        buttonsaveproveedor.setGeometry(30,280,460,30)
        buttonsaveproveedor.setText("Guardar")
        buttonsaveproveedor.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsaveproveedor.clicked.connect(lambda: self.savecompra(token))

        self.img = QLabel(tab)
        self.img.setGeometry(700,30,400,400)
    def fieldselected(self,type):
        self.fileFrame = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.fileFrame.setWindowTitle("Archivo para imagen")
        self.fileFrame.setFixedSize(320, 200)
        self.openFileNameDialog(type)
    def openFileNameDialog(self,type):

        options = QFileDialog.Options()
        self.rutaimg, __ = QFileDialog.getOpenFileName(self.fileFrame,"Seleccione el ticket de la compra", "","All Files (*);;PNG,JPG,JPEG Image(*.png,*.jpg,*.jpeg)", options=options)

        if self.rutaimg:
            saveImgClient = QPixmap(self.rutaimg)
            imgclient = saveImgClient.scaled(240,240)

            if(type == 1):
                self.img.setPixmap(imgclient) # ver imagen en create cliente
            elif(type == 2):
                self.imgedit.setPixmap(imgclient)
    def savecompra(self,token):
        if(self.txtcantidad.text() == ''):
            self.msm.messageError("Campo requerido","La cantidad de productos a comprar es requerido")
        elif(self.txtpricetotal.text() == ''):
            self.msm.messageError("Campo requerido","El precio total de la compra es requerido")
        elif(self.selectproduct.currentText() == 'Seleccione un producto'):
            self.msm.messageError("Campo requerido","Seleccione un producto")
        elif(self.selectpromotor.currentText() == 'Seleccione un promotor'):
            self.msm.messageError("Campo requerido","Seleccione un promotor")
        else:
            args = {"api_token":token,"stock":self.txtcantidad.text(),"precio":self.txtpricetotal.text(),"product":self.selectproduct.currentText(),"promotor":self.selectpromotor.currentText(),"userid":self.userid}

            if(self.rutaimg != ''):
                files = {'img': open(self.rutaimg,'rb')}
            else:
                files = "";

            guardar = self.msm.messageConfirm("Guardar Compra","¿Quieres guardar la compra?")

            if(guardar == True):
                compra = self.ctrcompra.store(args,files)
                if(compra['code'] == 200):
                    self.limpiarinput(token)
                self.msm.messageInfo("Usuario " + compra['status'], compra['msm']);
    def limpiarinput(self,token):
        self.txtcantidad.clear()
        self.txtpricetotal.clear()
        self.selectproduct.clear()
        self.selectpromotor.clear()
        self.img.clear()
        self.rutaimg = "";
        self.selectproduct.addItem("Seleccione un producto")
        self.selectproduct.addItems(self.productos)
        self.selectpromotor.addItem("Seleccione un promotor")
        self.selectpromotor.addItems(self.promotores)
    def generatetext(self,numerocandenas,tamanio):
        for x in range(numerocandenas):
            return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(tamanio))
    def edit(self,token,user,data):

        self.frameedit = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.frameedit.setWindowModality(Qt.ApplicationModal)
        self.frameedit.setWindowTitle("Modificar la compra con tiket " + data[1])
        self.frameedit.setWindowIcon(QIcon('icon/tienda.png'))
        self.frameedit.setFixedSize(800, 350)

        self.idcompraedit = data[0]

        productos = self.ctrcompra.loadingproducts(token)
        promotores = self.ctrcompra.loadingpromotor(token)
        self.useridedit = user
        if(productos['code'] == 200):
            for product in productos['data']:
                self.productos.append(product['nombre'])
        if(promotores['code'] == 200):
            for promotor in promotores['data']:
                self.promotores.append(promotor['nombre'])

        labelcantidadedit = QLabel("Cantidad: ", self.frameedit)
        labelcantidadedit.setGeometry(30,30,100,30)

        self.txtcantidadedit = QLineEdit(self.frameedit)
        self.txtcantidadedit.setGeometry(90,30,400,30)
        self.txtcantidadedit.setMaxLength(10)
        self.txtcantidadedit.setText(data[2])
        self.txtcantidadedit.setValidator(QtGui.QIntValidator())

        labelpreciototaledit = QLabel("Precio total: ", self.frameedit)
        labelpreciototaledit.setGeometry(30,80,100,30)

        self.txtpricetotaledit = QLineEdit(self.frameedit)
        self.txtpricetotaledit.setGeometry(90,80,400,30)
        self.txtpricetotaledit.setMaxLength(10)
        self.txtpricetotaledit.setText(data[3])
        self.txtpricetotaledit.setValidator(QtGui.QDoubleValidator())

        labelimgedit = QLabel("Ticket: ", self.frameedit)
        labelimgedit.setGeometry(30,130,100,30)

        buttonimgedit = QPushButton(self.frameedit)
        buttonimgedit.setGeometry(90,130,400,30)
        buttonimgedit.setIcon(QIcon('icon/seleccione.png'))
        buttonimgedit.setText("Seleccione Foto")
        buttonimgedit.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimgedit.clicked.connect(lambda: self.fieldselected(2))

        labelproductoedit = QLabel("Producto: ", self.frameedit)
        labelproductoedit.setGeometry(30,180,100,30)

        self.selectproductedit = QComboBox(self.frameedit)
        self.selectproductedit.addItem("Seleccione un producto")
        self.selectproductedit.addItems(self.productos)
        self.selectproductedit.setGeometry(90,180,400,30)

        indexpositionproduct = 0;
        for i,product in enumerate(self.productos):
            if(data[6] == product):
                indexpositionproduct = i + 1
        self.selectproductedit.setCurrentIndex(indexpositionproduct)

        labelpromotoredit = QLabel("Promotor: ", self.frameedit)
        labelpromotoredit.setGeometry(30,230,100,30)

        self.selectpromotoredit = QComboBox(self.frameedit)
        self.selectpromotoredit.addItem("Seleccione un promotor")
        self.selectpromotoredit.addItems(self.promotores)
        self.selectpromotoredit.setGeometry(90,230,400,30)

        indexpositionpromotor = 0;
        for i,promotor in enumerate(self.promotores):
            if(data[5] == promotor):
                indexpositionpromotor = i + 1
        self.selectpromotoredit.setCurrentIndex(indexpositionpromotor)

        buttonsaveproveedoredit = QPushButton(self.frameedit)
        buttonsaveproveedoredit.setGeometry(30,280,460,30)
        buttonsaveproveedoredit.setText("Guardar")
        buttonsaveproveedoredit.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsaveproveedoredit.clicked.connect(lambda: self.saveupdatecompra(token))

        self.imgedit = QLabel(self.frameedit)
        self.imgedit.setGeometry(530,10,300,300)

        self.frameedit.exec_()
    def saveupdatecompra(self,token):

        if(self.txtcantidadedit.text() == ''):
            self.msm.messageError("Campo requerido","La cantidad de productos a comprar es requerido")
        elif(self.txtpricetotaledit.text() == ''):
            self.msm.messageError("Campo requerido","El precio total de la compra es requerido")
        elif(self.selectproductedit.currentText() == 'Seleccione un producto'):
            self.msm.messageError("Campo requerido","Seleccione un producto")
        elif(self.selectpromotoredit.currentText() == 'Seleccione un promotor'):
            self.msm.messageError("Campo requerido","Seleccione un promotor")
        else:
            args = {"api_token":token,"id":self.idcompraedit,"stock":self.txtcantidadedit.text(),"precio":self.txtpricetotaledit.text(),"producto":self.selectproductedit.currentText(),"promotor":self.selectpromotoredit.currentText(),"user":self.useridedit}

            if(self.rutaimg != ''):
                files = {'img': open(self.rutaimg,'rb')}
            else:
                files = "";

            guardar = self.msm.messageConfirm("Guardar Compra","¿Quieres guardar la compra?")

            if(guardar == True):
                compraedit = self.ctrcompra.update(args,files)
                if(compraedit['code'] == 200):
                    self.tableRefresh.clearContents()
                    datos = self.getcompras(token,1,20)
                    self.table(self.tableRefresh,datos['data'])
                    self.frameedit.close()
                self.msm.messageInfo("Usuario " + compraedit['status'], compraedit['msm']);
    def delete(self,token,data):
        confirm = self.msm.messageConfirm("Confirmar eliminar a " + data[1],"¿Quieres continuar con la eliminacion de la compra?")

        if(confirm):
            compra = self.ctrcompra.delete(token,data[0])
            if(compra['code'] == 200):
                self.msm.messageInfo("Compra " + compra['status'],compra['msm'])
                self.tableRefresh.clearContents()
                datos = self.getcompras(token,1,20)
                self.table(self.tableRefresh,datos['data'])
