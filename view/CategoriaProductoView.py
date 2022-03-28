from PyQt5.QtGui import QIcon,QFont
from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from view.Errors import ErrorGeneral
from controller import CategoriaProductoController


class CategoriaProductoView:
    def __init__(self):
        self.ctrcategoriaproducto = CategoriaProductoController.CategoriaProductoController()
        self.msm = ErrorGeneral.ErrorGeneral()
    def getcategorias(self,token,pagina,registropagina):
        datatable = self.ctrcategoriaproducto.getcategorias(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable;
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data;

        for i,d in enumerate(self.dataRefresh):
            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(d['nombre']))
    def createview(self,token,tab):
        labelnombre = QLabel("Nombre: ", tab)
        labelnombre.setGeometry(30,30,100,30)

        self.txtnombre = QLineEdit(tab)
        self.txtnombre.setGeometry(80,30,400,30)

        btnGuardar = QPushButton("Guardar",tab)
        btnGuardar.setGeometry(30,80,450,30)
        btnGuardar.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        btnGuardar.clicked.connect(lambda: self.validastore(self.txtnombre.text(),token))
    def validastore(self,nombre,token):
        if(nombre != ''):
            result = self.ctrcategoriaproducto.store(nombre,token)
            if(result['code'] == 200):
                datos = self.getcategorias(token,1,20)
                self.table(self.tableRefresh,datos['data'])
                self.msm.messageInfo("Categoria guardada", "El registro de categoria fue guardado con exito")
                self.txtnombre.clear()
            else:
                self.msm.messageError("Error al guardar categoria", "No se pudo guardar la categoria, intente mas tarde")
        else:
            self.msm.messageInfo("Campo requerido","Escribe el nombre de la categoria para continuar")
    def edit(self,token,data):
        self.editframe = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.editframe.setWindowTitle("Modificar la categoria de producto " + data[1])
        self.editframe.setWindowIcon(QIcon('icon/tienda.png'))
        self.editframe.setFixedSize(500, 150)

        labelname = QLabel("Nombre: ", self.editframe)
        labelname.setGeometry(30,30,100,30)

        txtname = QLineEdit(self.editframe)
        txtname.setText(data[1])
        txtname.setGeometry(80,30,400,30)

        btnsaveupdate = QPushButton(self.editframe)
        btnsaveupdate.setText("Guardar")
        btnsaveupdate.setGeometry(30,80,450,30)
        btnsaveupdate.setStyleSheet("QPushButton{background: #0000ff; color:#fff} QPushButton:hover{background:#00008a; color:#fff;}")
        btnsaveupdate.clicked.connect(lambda: self.update(token,data[0],txtname.text()))

        self.editframe.exec_()
    def update(self,token,id,nombre):

        confirm = self.msm.messageConfirm("Confirmar en guardar categoria producto","¿Quieres continuar con la modificacion de la categoria de producto?")

        if(confirm):
            categoria = self.ctrcategoriaproducto.update(token,id,nombre)

            if(categoria['code'] == 200):
                self.msm.messageInfo("Categoria producto " + categoria['status'],categoria['msm'])
                self.tableRefresh.clearContents()
                datos = self.getcategorias(token,1,20)
                self.table(self.tableRefresh,datos['data'])
                self.editframe.close()
            else:
                self.msm.messageError("Categoria producto " + categoria['status'],categoria['msm'])
    def delete(self,token,data):

        confirm = self.msm.messageConfirm("Confirmar eliminar " + data[1],"¿Quieres continuar con la eliminacion de la categoria de producto?")

        if(confirm):

            categoria = self.ctrcategoriaproducto.delete(token,data[0])

            if(categoria['code'] == 200):
                self.msm.messageInfo("Categoria producto " + categoria['status'],categoria['msm'])
                self.tableRefresh.clearContents()
                datos = self.getcategorias(token,1,20)
                self.table(self.tableRefresh,datos['data'])
