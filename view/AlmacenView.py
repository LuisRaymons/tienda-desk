from PyQt5.QtGui import QIcon,QFont
from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view.Errors import ErrorGeneral
from controller import AlmacenController


class AlmacenView:
    def __init__(self):
        self.ctralmacen = AlmacenController.AlmacenController()
        self.msm = ErrorGeneral.ErrorGeneral()
    def getalmacenes(self,token,pagina,registropagina):
        datatable = self.ctralmacen.getalmacenes(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data;
        for i,d in enumerate(self.dataRefresh):
            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(str(d['entrada'])))
            self.tableRefresh.setItem(i, 2, QTableWidgetItem(str(d['salida'])))
            self.tableRefresh.setItem(i, 3, QTableWidgetItem(str(d['stock'])))
            self.tableRefresh.setItem(i, 4, QTableWidgetItem(d['usuario']))
            self.tableRefresh.setItem(i, 5, QTableWidgetItem(d['producto']))
    def edit(self,token,data):
        self.frameedit = QDialog(None, QtCore.Qt.WindowCloseButtonHint)
        self.frameedit.setWindowModality(Qt.ApplicationModal)
        self.frameedit.setWindowTitle("Modificar los stock de producto " + data[5])
        self.frameedit.setWindowIcon(QIcon('icon/tienda.png'))
        self.frameedit.setFixedSize(550, 250)

        self.idalmacenedit = data[0]
        self.productselected = data[5]

        labelentradas = QLabel("Entradas: ",self.frameedit)
        labelentradas.setGeometry(30,30,100,30)

        self.txtentradas = QLineEdit(self.frameedit)
        self.txtentradas.setText(data[1])
        self.txtentradas.setMaxLength(10)
        self.txtentradas.setValidator(QtGui.QDoubleValidator())
        self.txtentradas.setGeometry(100,30,400,30)

        labelsalidas = QLabel("Salidas: ",self.frameedit)
        labelsalidas.setGeometry(30,80,100,30)

        self.txtsalidas = QLineEdit(self.frameedit)
        self.txtsalidas.setText(data[2])
        self.txtsalidas.setMaxLength(10)
        self.txtsalidas.setValidator(QtGui.QDoubleValidator())
        self.txtsalidas.setGeometry(100,80,400,30)

        labelstock = QLabel("Stock: ", self.frameedit)
        labelstock.setGeometry(30,130,100,30)

        self.txtstock  = QLineEdit(self.frameedit)
        self.txtstock.setText(data[3])
        self.txtstock.setMaxLength(10)
        self.txtstock.setValidator(QtGui.QDoubleValidator())
        self.txtstock.setGeometry(100,130,400,30)

        btnguardar = QPushButton(self.frameedit)
        btnguardar.setGeometry(30,180,450,30)
        btnguardar.setText("Guardar")
        btnguardar.setStyleSheet("QPushButton{background: #0000e6; color:#fff} QPushButton:hover{background:#000088; color:#fff;}")
        btnguardar.clicked.connect(lambda: self.updatealmacen(token))

        self.frameedit.exec_()

    def updatealmacen(self,token):

        args = {"api_token":token,"id":self.idalmacenedit,"entry":self.txtentradas.text(),"exit":self.txtsalidas.text(),"stock":self.txtstock.text()}

        guardar = self.msm.messageConfirm("Guardar producto","¿Quieres guardar el registro de almacen?")
        if(guardar == True):
            almacenedit = self.ctralmacen.update(args)
            if(almacenedit['code'] == 200):
                self.tableRefresh.clearContents()
                datos = self.getalmacenes(token,1,20)
                self.table(self.tableRefresh,datos['data'])
                self.frameedit.close()
            self.msm.messageInfo("Almacen " + almacenedit['status'], almacenedit['msm']);
