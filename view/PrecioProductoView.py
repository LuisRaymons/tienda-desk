from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view.Errors import ErrorGeneral
from controller import PrecioProducto

from config import env
import cv2
import os
import numpy as np
from PIL import Image


class PrecioProductoView:
    def __init__(self):
        self.ctrproductoprecio = PrecioProducto.PrecioProducto()
        self.msm = ErrorGeneral.ErrorGeneral()
        self.missingproduct = []
    def getproductosprecio(self,token,pagina,registropagina):
        datatable = self.ctrproductoprecio.getproductosprecio(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data;

        for i,d in enumerate(self.dataRefresh):

            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(d['nombre']))
            self.tableRefresh.setItem(i, 2, QTableWidgetItem(str(d['precio'])))
    def createview(self,token,tab):

        labelproducto = QLabel("Producto", tab)
        labelproducto.setGeometry(30,30,100,30)

        self.selectproduct = QComboBox(tab)
        self.selectproduct.setGeometry(100,30,400,30)
        self.selectproduct.addItem("Seleccione un producto")

        productosmissing = self.ctrproductoprecio.missing(token)
        if(productosmissing['code'] == 200):
            datos = productosmissing['data']
            for missing in datos:
                self.selectproduct.addItem(missing['nombre'])

        labelprecio = QLabel("Precio",tab)
        labelprecio.setGeometry(30,80,100,30)

        self.txtprecio = QLineEdit(tab)
        self.txtprecio.setMaxLength(10)
        self.txtprecio.setValidator(QtGui.QDoubleValidator())
        self.txtprecio.setGeometry(100,80,400,30)

        buttonsavemissing = QPushButton(tab)
        buttonsavemissing.setGeometry(30,130,460,30)
        buttonsavemissing.setText("Guardar")
        buttonsavemissing.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsavemissing.clicked.connect(lambda: self.savemissing(token))
    def savemissing(self,token):

        producto = self.selectproduct.currentText()
        precio = self.txtprecio.text()

        if(producto == 'Seleccione un producto'):
            self.msm.messageInfo("Campo requerido","Seleccione un producto para agregar su precio")
        elif(precio == ''):
            self.msm.messageInfo("Campo requerido","Escriba el precio del producto")
        else:
            guardar = self.msm.messageConfirm("Guardar producto","¿Quieres guardar el precio del producto?")

            if(guardar == True):
                args = {"api_token":token,"product":producto,"price":precio}
                precioproduct = self.ctrproductoprecio.store(args)
                if(precioproduct['code'] == 200):

                    self.inputclear(token)
                    datos = self.getproductosprecio(token,1,20)
                    #self.tableRefresh.clearContents()
                    #self.table(self.tableRefresh,datos['data'])

                self.msm.messageInfo("Producto " + precioproduct['status'], precioproduct['msm']);
    def edit(self,token,data):

        self.frameedit = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.frameedit.setWindowModality(Qt.ApplicationModal)
        self.frameedit.setWindowTitle("Modificar al producto " + data[1])
        self.frameedit.setWindowIcon(QIcon('icon/tienda.png'))
        self.frameedit.setFixedSize(550, 200)

        self.ideditproductoprecio = data[0]

        labelproductoedit = QLabel("Producto", self.frameedit)
        labelproductoedit.setGeometry(30,30,100,30)

        self.selectproductedit = QLineEdit(self.frameedit)
        self.selectproductedit.setGeometry(100,30,400,30)
        self.selectproductedit.setText(data[1])

        labelprecioedit = QLabel("Precio",self.frameedit)
        labelprecioedit.setGeometry(30,80,100,30)

        self.txtprecioedit = QLineEdit(self.frameedit)
        self.txtprecioedit.setMaxLength(10)
        self.txtprecioedit.setText(data[2])
        self.txtprecioedit.setValidator(QtGui.QDoubleValidator())
        self.txtprecioedit.setGeometry(100,80,400,30)

        buttonsavemissing = QPushButton(self.frameedit)
        buttonsavemissing.setGeometry(30,130,460,30)
        buttonsavemissing.setText("Guardar")
        buttonsavemissing.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsavemissing.clicked.connect(lambda: self.savemissingupdate(token))

        self.frameedit.show()
    def delete(self,token,data):
        confirm = self.msm.messageConfirm("Confirmar eliminar a " + data[1],"¿Quieres continuar con la eliminacion del precio del productos?")

        if(confirm == True):
            args = {"api_token":token,"id":data[0]}
            precioproduct = self.ctrproductoprecio.delete(args)

            self.msm.messageInfo("Precio de productos " + precioproduct['status'],precioproduct['msm'])
    def savemissingupdate(self,token):
        product = self.selectproductedit.text()
        precio = self.txtprecioedit.text();

        if(product == ""):
            self.msm.messageInfo("Campo requerido","Seleccione un producto para agregar su precio")
        elif(precio == ""):
            self.msm.messageInfo("Campo requerido","Escriba el precio del producto")
        else:
            guardar = self.msm.messageConfirm("Guardar producto","¿Quieres guardar el precio del producto?")

            if(guardar == True):
                args = {"api_token":token,"id":self.ideditproductoprecio,"price":precio}

                precioproduct = self.ctrproductoprecio.update(args)
                if(precioproduct['code'] == 200):

                    self.frameedit.close()
    def inputclear(self,token):
        self.txtprecio.clear()
        self.selectproduct.clear()
        self.selectproduct.addItem("Seleccione un producto")

        productosmissing = self.ctrproductoprecio.missing(token)
        if(productosmissing['code'] == 200):
            datos = productosmissing['data']
            for missing in datos:
                self.selectproduct.addItem(missing['nombre'])
