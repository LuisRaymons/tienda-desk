from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view.Errors import ErrorGeneral
from controller import ProductoController

from config import env
import cv2
import os
import imutils
import numpy as np
from PIL import Image


class ProductoView:
    def __init__(self):
        self.ctrproducto = ProductoController.ProductoController()
        self.msm = ErrorGeneral.ErrorGeneral()
        self.categorias = []
        self.rutaimg = ""
        self.rutaimgedit = ""
    def getproductos(self,token,pagina,registropagina):
        datatable = self.ctrproducto.getproductos(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data;

        for i,d in enumerate(self.dataRefresh):

            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(d['nombrepoducto']))
            self.tableRefresh.setItem(i, 2, QTableWidgetItem(d['descripcion']))
            self.tableRefresh.setItem(i, 3, QTableWidgetItem(d['precioPorKilo']))
            self.tableRefresh.setItem(i, 4, QTableWidgetItem(QtGui.QIcon(QtGui.QPixmap(env.URLRESOURCE + str(d['img']))),env.URLRESOURCE + str(d['img']),1))
            self.tableRefresh.setItem(i, 5, QTableWidgetItem(d['nombrecategoria']))
    def createview(self,token,tab):
        categorias = self.ctrproducto.loadingcategorias(token)
        if(categorias['code'] == 200):
            for c in categorias['data']:
                self.categorias.append(c['nombre'])

        labelnombre = QLabel("Nombre: ",tab)
        labelnombre.setGeometry(30,30,100,30)

        self.txtnombre = QLineEdit(tab)
        self.txtnombre.setGeometry(100,30,400,30)

        labeldescripcon = QLabel("Descripcion: ", tab)
        labeldescripcon.setGeometry(30,80,100,30)

        self.txtdescripcion = QPlainTextEdit(tab)
        self.txtdescripcion.move(20,20)
        self.txtdescripcion.resize(400,200)
        self.txtdescripcion.setGeometry(100,80,400,100)

        labelpreciokilo = QLabel("Precio Kilo:",tab)
        labelpreciokilo.setGeometry(30,200,100,30)

        self.checkpreciokilo = QCheckBox(tab)
        self.checkpreciokilo.setGeometry(100,200,400,30)

        labelimagen = QLabel("Imagen: ",tab)
        labelimagen.setGeometry(30,250,100,30)

        buttonimg = QPushButton(tab)
        buttonimg.setGeometry(100,250,400,30)
        buttonimg.setIcon(QIcon('icon/seleccione.png'))
        buttonimg.setText("Seleccione Foto")
        buttonimg.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimg.clicked.connect(lambda: self.fieldselected(1))

        labelcategoria = QLabel("Categoria: ", tab)
        labelcategoria.setGeometry(30,300,100,30)

        self.selectcategorias = QComboBox(tab)
        self.selectcategorias.addItem("Seleccione una categoria")
        self.selectcategorias.addItems(self.categorias)
        self.selectcategorias.setGeometry(100,300,400,30)

        buttonsaveproduct = QPushButton(tab)
        buttonsaveproduct.setText("Guardar")
        buttonsaveproduct.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsaveproduct.setGeometry(30,350,470,30)
        buttonsaveproduct.clicked.connect(lambda: self.storeproduct(token))

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
            saveImgClient = QPixmap(self.rutaimg)
            imgclient = saveImgClient.scaled(240,240)

            if(type == 1):
                self.img.setPixmap(imgclient) # ver imagen en create cliente
            elif(type == 2):
                self.imgedit.setPixmap(imgclient)
    def storeproduct(self,token):
        if(self.txtnombre.text() == ''):
            self.msm.messageError("Campo requerido","El nombre del producto es requerido")
        elif(self.txtdescripcion.toPlainText() == ''):
            self.msm.messageError("Campo requerido","El nombre del producto es requerido")
        elif(self.selectcategorias.currentText() == 'Seleccione una categoria'):
            self.msm.messageError("Campo requerido","Seleccione una categoria")
        else:
            pricekilo = 'true' if(self.checkpreciokilo.isChecked()) else 'false'
            args = {"api_token":token,"name":self.txtnombre.text(),"description":self.txtdescripcion.toPlainText(),"categoria":self.selectcategorias.currentText(),"pricekilo":pricekilo}

            if(self.rutaimg == ''):
                files = {}
            else:
                files = {'img': open(self.rutaimg,'rb')}

            guardar = self.msm.messageConfirm("Guardar producto","¿Quieres guardar al producto?")
            if(guardar == True):
                product = self.ctrproducto.store(args,files)
                if(product['code'] == 200):
                    self.limpiarinput()
                    self.tableRefresh.clearContents()
                    datos = self.getproductos(token,1,20)
                    self.table(self.tableRefresh,datos['data'])
                self.msm.messageInfo("Producto " + product['status'], product['msm']);
    def limpiarinput(self):
        self.txtnombre.clear()
        self.txtdescripcion.clear()
        self.checkpreciokilo.setChecked(False)
        self.selectcategorias.clear()
        self.selectcategorias.addItem("Seleccione una categoria")
        self.selectcategorias.addItems(self.categorias)
        self.img.clear()
        self.rutaimg = ""
    def edit(self,token,data):
        self.frameedit = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.frameedit.setWindowModality(Qt.ApplicationModal)
        self.frameedit.setWindowTitle("Modificar al producto " + data[1])
        self.frameedit.setWindowIcon(QIcon('icon/tienda.png'))
        self.frameedit.setFixedSize(800, 500)

        self.ideditproducto = data[0]

        categorias = self.ctrproducto.loadingcategorias(token)
        self.categorias.clear()
        if(categorias['code'] == 200):
            for c in categorias['data']:
                self.categorias.append(c['nombre'])

        labelnombreedit = QLabel("Nombre: ",self.frameedit)
        labelnombreedit.setGeometry(30,30,100,30)

        self.txtnombreedit = QLineEdit(self.frameedit)
        self.txtnombreedit.setText(data[1])
        self.txtnombreedit.setGeometry(100,30,400,30)

        labeldescripconedit = QLabel("Descripcion: ", self.frameedit)
        labeldescripconedit.setGeometry(30,80,100,30)

        self.txtdescripcionedit = QPlainTextEdit(self.frameedit)
        self.txtdescripcionedit.move(20,20)
        self.txtdescripcionedit.resize(400,200)
        self.txtdescripcionedit.insertPlainText(data[2])
        self.txtdescripcionedit.setGeometry(100,80,400,100)

        labelpreciokiloedit = QLabel("Precio Kilo:",self.frameedit)
        labelpreciokiloedit.setGeometry(30,200,100,30)

        self.checkpreciokiloedit = QCheckBox(self.frameedit)
        if(data[3] == 'true'):
            self.checkpreciokiloedit.setChecked(True)
        self.checkpreciokiloedit.setGeometry(100,200,400,30)

        labelimagenedit = QLabel("Imagen: ",self.frameedit)
        labelimagenedit.setGeometry(30,250,100,30)

        buttonimgedit = QPushButton(self.frameedit)
        buttonimgedit.setGeometry(100,250,400,30)
        buttonimgedit.setIcon(QIcon('icon/seleccione.png'))
        buttonimgedit.setText("Seleccione Foto")
        buttonimgedit.setStyleSheet("QPushButton{background: #ff851c; color:#fff} QPushButton:hover{background:#ff741c; color:#fff;}")
        buttonimgedit.clicked.connect(lambda: self.fieldselected(2))

        labelcategoriaedit = QLabel("Categoria: ", self.frameedit)
        labelcategoriaedit.setGeometry(30,300,100,30)

        self.selectcategoriasedit = QComboBox(self.frameedit)
        self.selectcategoriasedit.addItem("Seleccione una categoria")
        self.selectcategoriasedit.addItems(self.categorias)
        self.selectcategoriasedit.setGeometry(100,300,400,30)
        indexposition = 0
        for i,categoria in enumerate(self.categorias):
            if(data[5].strip() == categoria.strip()):
                indexposition = i + 1
        self.selectcategoriasedit.setCurrentIndex(indexposition)

        buttonsaveproductedit = QPushButton(self.frameedit)
        buttonsaveproductedit.setText("Guardar")
        buttonsaveproductedit.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        buttonsaveproductedit.setGeometry(30,350,470,30)
        buttonsaveproductedit.clicked.connect(lambda: self.updateproduct(token))

        self.imgedit = QLabel(self.frameedit)
        self.imgedit.setGeometry(550,30,400,400)

        self.frameedit.exec_()
    def updateproduct(self,token):

        pricekilo = 'true' if(self.checkpreciokiloedit.isChecked()) else 'false'
        args = {"api_token":token,"id":self.ideditproducto,"name":self.txtnombreedit.text(),"description":self.txtdescripcionedit.toPlainText(),"categoria":self.selectcategoriasedit.currentText(),"pricekilo":pricekilo}

        if(self.rutaimgedit == ''):
            files = {}
        else:
            files = {'img': open(self.rutaimgedit,'rb')}

        guardar = self.msm.messageConfirm("Guardar producto","¿Quieres guardar al producto?")
        if(guardar == True):
            productedit = self.ctrproducto.update(args,files)
            if(productedit['code'] == 200):
                self.tableRefresh.clearContents()
                datos = self.getproductos(token,1,20)
                self.table(self.tableRefresh,datos['data'])
                self.frameedit.close()
                self.rutaimg = ""
            self.msm.messageInfo("Producto " + productedit['status'], productedit['msm']);
    def delete(self,token,data):
        confirm = self.msm.messageConfirm("Confirmar eliminar a " + data[1],"¿Quieres continuar con la eliminacion del producto?")

        if(confirm):
            producto = self.ctrproducto.delete(token,data[0])
            if(producto['code'] == 200):
                self.msm.messageInfo("Producto " + producto['status'],producto['msm'])
                self.tableRefresh.clearContents()
                datos = self.getproductos(token,1,20)
                self.table(self.tableRefresh,datos['data'])
