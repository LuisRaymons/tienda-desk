from PyQt5.QtGui import QIcon,QFont
from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtCore import Qt as tr
from PyQt5.QtWidgets import *
from view.Errors import ErrorGeneral
from controller import VentaController
import json


class VentaView:
    def __init__(self):
        self.ctrventa = VentaController.VentaController()
        self.msm = ErrorGeneral.ErrorGeneral()
        self.clientes = []
        self.productos = []
        self.pagos = []
        self.datostablaproduct = []
        self.totalventa = 0.00
    def getventas(self,token,pagina,registropagina):
        datatable = self.ctrventa.getventas(token,pagina,registropagina)
        if(datatable['code'] == 200):
            return datatable
    def table(self,table,data):
        self.tableRefresh = table
        self.dataRefresh = data;
        for i,d in enumerate(self.dataRefresh):
            self.tableRefresh.setItem(i, 0, QTableWidgetItem(str(d['id'])))
            self.tableRefresh.setItem(i, 1, QTableWidgetItem(d['factura']))
            self.tableRefresh.setItem(i, 2, QTableWidgetItem(d['precio_total']))
            self.tableRefresh.setItem(i, 3, QTableWidgetItem(d['tipopago']))
            self.tableRefresh.setItem(i, 4, QTableWidgetItem(d['cliente']))
            self.tableRefresh.setItem(i, 5, QTableWidgetItem(d['usuario']))
    def createview(self,token,tab,userid):
        clientes = self.ctrventa.loadingcliente(token)
        productos = self.ctrventa.loadingproductos(token)
        pagos = self.ctrventa.loadingpagos()

        if(clientes['code'] == 200):
            for cliente in clientes['data']:
                self.clientes.append(cliente['nombre'])
        if(productos['code'] == 200):
            for producto in productos['data']:
                self.productos.append(producto['nombre'])
        if(pagos['code'] == 200):
            for pago in pagos['data']:
                self.pagos.append(pago['name'])

        labelcliente = QLabel("Cliente: ", tab)
        labelcliente.setGeometry(30,30,100,30)

        self.selectcliente = QComboBox(tab)
        self.selectcliente.setGeometry(100,30,450,30)
        self.selectcliente.addItem("Selecciona cliente")
        self.selectcliente.addItems(self.clientes)

        labelproducto = QLabel("Producto", tab)
        labelproducto.setGeometry(30,80,100,30)

        self.selectproduct = QComboBox(tab)
        self.selectproduct.setGeometry(100,80,350,30)
        self.selectproduct.addItem("Seleccione el producto")
        self.selectproduct.addItems(self.productos)

        buttonaddproduct = QPushButton(tab)
        buttonaddproduct.setText("Agregar")
        buttonaddproduct.setGeometry(470,80,80,30)
        buttonaddproduct.clicked.connect(lambda: self.addproductitem(token))

        labelpago = QLabel("Tipo de pago",tab)
        labelpago.setGeometry(30,130,100,30)

        self.selectpago = QComboBox(tab)
        self.selectpago.setGeometry(100,130,450,30)
        self.selectpago.addItem("Seleccione el tipo de pago")
        self.selectpago.addItems(self.pagos)

        btnsaveventa = QPushButton(tab)
        btnsaveventa.setGeometry(30,180,500,30)
        btnsaveventa.setText("Pagar")
        btnsaveventa.setStyleSheet("QPushButton{background: #0000ff; color:#fff} QPushButton:hover{background:#00008a; color:#fff;}")
        btnsaveventa.clicked.connect(lambda: self.pagarventa(token,userid))

        self.tableproduct = QtWidgets.QTableWidget(tab)
        self.tableproduct.setGeometry(QtCore.QRect(560, 30, 550, 600))
        self.tableproduct.setColumnCount(5)
        self.tableproduct.setRowCount(int(20))
        self.tableproduct.setHorizontalHeaderLabels(['id','nombre','cantidad','precio',"precio total"])
        self.tableproduct.setAlternatingRowColors(True)
        self.tableproduct.setWordWrap(False)
        self.tableproduct.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableproduct.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableproduct.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableproduct.horizontalHeader().setStretchLastSection(True)
        self.tableproduct.setContextMenuPolicy(tr.CustomContextMenu)
        self.tableproduct.customContextMenuRequested.connect(self.menutable)
    def addproductitem(self,token):

        producto = self.selectproduct.currentText()
        if(producto == 'Seleccione el producto'):
            self.msm.messageError("Seleccione un producto", "Necesitas seleccionar un producto para poder agregarlo al carrito")
        else:
            self.frameadditeminit = QDialog()
            self.frameadditeminit.setWindowTitle("Agregar producto de " + producto)
            self.frameadditeminit.setFixedSize(320, 200)

            labelitems = QLabel("Cantidad: ", self.frameadditeminit)
            labelitems.setGeometry(30,30,100,30)

            txtcantidad = QLineEdit(self.frameadditeminit)
            txtcantidad.setGeometry(90,30,200,30)
            txtcantidad.setMaxLength(10)
            txtcantidad.setText(str(1))
            txtcantidad.setValidator(QtGui.QDoubleValidator())

            buttonaddproduct = QPushButton(self.frameadditeminit)
            buttonaddproduct.setGeometry(30,80,260,30)
            buttonaddproduct.setText("Agregar")
            buttonaddproduct.clicked.connect(lambda: self.additemproductfunction(token,producto,txtcantidad.text(),1))

            self.frameadditeminit.show()
    def actualizarproductostable(self):
        self.tableproduct.clearContents()

        for i,d in enumerate(self.datostablaproduct):
            self.tableproduct.setItem(i,0,QTableWidgetItem(str(d['id'])))
            self.tableproduct.setItem(i,1,QTableWidgetItem(d['nombre']))
            self.tableproduct.setItem(i,2,QTableWidgetItem(str(d['cantidad'])))
            self.tableproduct.setItem(i,3,QTableWidgetItem(str(d['precio'])))
            self.tableproduct.setItem(i,4,QTableWidgetItem(str(d['precioTotal'])))
    def editproducttableproduct(self,item):

        self.frameadditems = QDialog()
        self.frameadditems.setWindowTitle("Modicar producto de " + item[1])
        self.frameadditems.setFixedSize(320, 200)

        labelitems = QLabel("Cantidad: ", self.frameadditems)
        labelitems.setGeometry(30,30,100,30)

        self.txtcantidad = QLineEdit(self.frameadditems)
        self.txtcantidad.setGeometry(90,30,200,30)
        self.txtcantidad.setMaxLength(10)
        self.txtcantidad.setText(str(item[2]))
        self.txtcantidad.setValidator(QtGui.QDoubleValidator())

        buttonaddproduct = QPushButton(self.frameadditems)
        buttonaddproduct.setGeometry(30,80,260,30)
        buttonaddproduct.setText("Agregar") # (self,token,product,cantidad,type)}
        buttonaddproduct.clicked.connect(lambda: self.additemproductfunction("",item[1],self.txtcantidad.text(),2))

        self.frameadditems.show();
    def deleteproducttableproduct(self,item):

        templist = []
        for i,producto in enumerate(self.datostablaproduct):
            if(producto['nombre'] != item[1]):
                templist.append(producto)
        self.datostablaproduct = templist
        self.actualizarproductostable()
    def additemproductfunction(self,token,product,cantidad,type):

        if(type == 1):
            product = self.ctrventa.searchproduct(token,product)
            cantidaditems = 1 if cantidad == '' else cantidad
            if(product['code'] == 200):
                datos = product['data']
                precio = self.ctrventa.searchprecoproducto(token,datos['id'])
                if(precio['code'] == 200):
                    datosprecio = precio['data']
                    preciobyproductocount = round(int(cantidaditems) * float(datosprecio['precio']));
                    self.totalventa = self.totalventa + preciobyproductocount
                    product = {"id":datos['id'],"nombre":datos['nombre'],"img":datos['img'],"precio":datosprecio['precio'],"cantidad": cantidaditems, "precioTotal": preciobyproductocount}
                    self.datostablaproduct.append(product)
                    self.frameadditeminit.close()
        else:
            templist = []
            self.totalventa = 0.00

            for i,producto in enumerate(self.datostablaproduct):
                precioTotal  = round(int(cantidad) * float(producto['precio'])) if (producto['nombre'] == product) else round(int(producto['cantidad']) * float(producto['precio']))

                if(producto['nombre'] == product):
                    dato = {"id":producto['id'],"nombre":producto['nombre'],"img":producto['img'],"precio":producto['precio'],"cantidad": cantidad, "precioTotal": precioTotal}
                else:
                    dato = {"id":producto['id'],"nombre":producto['nombre'],"img":producto['img'],"precio":producto['precio'],"cantidad": producto['cantidad'], "precioTotal": precioTotal}

                self.totalventa = self.totalventa + precioTotal

                templist.append(dato)
                self.frameadditems.close()
            self.datostablaproduct = templist;




        self.filterduplicados()
        self.actualizarproductostable()
    def pagarventa(self,token,user):

        cliente = 1 if self.selectcliente.currentText() == 'Selecciona cliente' else self.selectcliente.currentText()

        if(self.selectpago.currentText() == 'Efectivo'):

            if(len(self.datostablaproduct) > 0):
                confirm = self.msm.messageConfirm("Confirmar venta", "¿Deseas continuar con la venta?")
                if(confirm):
                    args = {"api_token":token,"cliente":cliente,"pago":1,"user":user,"datosventa":json.dumps(self.datostablaproduct),"totalventa":self.totalventa}
                    venta = self.ctrventa.store(args)

                    if(venta['code'] == 200):
                        self.msm.messageInfo("Venta " + venta['status'], venta['msm'])
                        self.limparinput(token)
            else:
                self.msm.messageError("No existen productos", "No se encontraron productos en el carrito")



    """ Function ayuda """
    def filterduplicados(self):
        tempr = []

        for producto in self.datostablaproduct:

            if producto not in tempr:
                tempr.append(producto)

        self.datostablaproduct = []
        self.datostablaproduct = tempr
    def menutable(self,position):

        indices = self.tableproduct.selectedIndexes()
        filaSeleccionada = [dato.text() for dato in self.tableproduct.selectedItems()]

        if(len(filaSeleccionada) > 1):
            if indices:
                menu = QMenu()
                updateMenu = menu.addAction(QIcon('icon/actualizar.ico'),"Modificar", lambda: self.editproducttableproduct(filaSeleccionada))
                menu.addSeparator()
                deleteproduct = menu.addAction(QIcon('icon/destroy.ico'),"Eliminar", lambda: self.deleteproducttableproduct(filaSeleccionada))
                menu.addSeparator()
                menu.exec_(self.tableproduct.viewport().mapToGlobal(position))
    def limparinput(self,token):
        self.selectcliente.clear()
        self.selectcliente.addItem("Selecciona cliente")
        self.selectcliente.addItems(self.clientes)
        self.selectproduct.clear()
        self.selectproduct.addItem("Seleccione el producto")
        self.selectproduct.addItems(self.productos)
        self.selectpago.clear()
        self.selectpago.addItem("Seleccione el tipo de pago")
        self.selectpago.addItems(self.pagos)
        self.datostablaproduct = []
        self.totalventa = 0.00
        self.tableproduct.clearContents()

        clientes = self.ctrventa.loadingcliente(token)
        productos = self.ctrventa.loadingproductos(token)
        pagos = self.ctrventa.loadingpagos()

        if(clientes['code'] == 200):
            for cliente in clientes['data']:
                self.clientes.append(cliente['nombre'])
        if(productos['code'] == 200):
            for producto in productos['data']:
                self.productos.append(producto['nombre'])
        if(pagos['code'] == 200):
            for pago in pagos['data']:
                self.pagos.append(pago['name'])
