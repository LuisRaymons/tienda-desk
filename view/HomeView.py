from PyQt5 import QtGui, QtCore,QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon,QFont
from pyqtgraph import PlotWidget, plot
from controller import HomeController
from view.Errors import ErrorGeneral
from view.Loading import Loading
from view import AlmacenView,CategoriaProductoView,ClienteView,CompraView,ProductoView,PromotorView,UsuarioView,VentaView,PrecioProductoView
import sys
import array
import math
import threading
import random
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class HomeView(QMainWindow):

    def __init__(self, data, loginview):

        self.login = data
        self.loginview = loginview
        self.pagina = 1;
        self.msm = ErrorGeneral.ErrorGeneral()
        self.ctrhome = HomeController.HomeController()
        self.viewalmacen = AlmacenView.AlmacenView()
        self.viewcategoria = CategoriaProductoView.CategoriaProductoView()
        self.viewcliente = ClienteView.ClienteView()
        self.viewcompre = CompraView.CompraView()
        self.viewproducto = ProductoView.ProductoView()
        self.viewpromotor = PromotorView.PromotorView()
        self.viewusuario = UsuarioView.UsuarioView()
        self.viewventa = VentaView.VentaView()
        self.viewprecioproduct = PrecioProductoView.PrecioProductoView()
        self.loading = Loading.Loading()

        super(HomeView, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(1300, 650)
        self.setWindowTitle("Tienda LRVA")
        self.setWindowIcon(QIcon('icon/tienda.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint);
        self.productexists = 0

        #Cargar charts
        self.charts()

        self.layoutmenu()
    def layoutmenu(self):

        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 200, 690))
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet("background-color: white;")

        self.treeWidget = QtWidgets.QTreeWidget(self.widget)
        self.treeWidget.setGeometry(QtCore.QRect(0, -25, 200, 690))
        self.treeWidget.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        self.treeWidget.setObjectName("treeWidget")
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)

        labelwelcome = QLabel("Bienvenido al sistema de tienda: ",self.widget)
        labelwelcome.setGeometry(15,220,230,10)
        labelwelcome.setStyleSheet("color: white; background-color: rgb(0,0,0)")

        # Mostrar datos de session
        labelname = QLabel(self.login['name'],self.widget)
        labelname.setGeometry(15,240,230,10)
        labelname.setStyleSheet("color: red; background-color: rgb(0,0,0)")

        labelcorreo = QLabel(self.login['email'],self.widget)
        labelcorreo.setGeometry(15,260,230,10)
        labelcorreo.setStyleSheet("color: red; background-color: rgb(0,0,0)")
        # self.frameTable.setStyleSheet("background-color: #fff")
        """
        labelface = QLabel(self.widget)
        labelface.setGeometry(15,280,230,200)
        pixmapface = QtGui.QPixmap(self.login['img'])
        labelface.setPixmap(pixmapface)
        """

        # Reloj label
        self.label = QLabel(self.widget)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 20, QFont.Bold))
        self.label.setGeometry(25,600,150,30)

        self.timer = QTimer(self.widget)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        #timer.setGeometry(QtCore.QRect(10, 600, 150, 30))

        self.treeWidget.headerItem().setForeground(0, brush)
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.treeWidget.customContextMenuRequested.connect(self.menuContextualmenu)

        self._translate = QtCore.QCoreApplication.translate
        self.widget.setWindowTitle(self._translate("Tienda LRVA", "Tienda LRVA"))
        self.treeWidget.headerItem().setText(0, self._translate("MainWindow", "Navigation"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)

        #menudatos = ["Dashboard","Categoria Producto","Cliente","Usuario","Producto","Almacen","Compra","Venta","Precio de producto","Cerrar Session"]
        menudatos = [{"name":"Dashboard", "iconfonst":"treeviewIcon/product-management.ico"},
                     {"name":"Categoria Producto", "iconfonst":"treeviewIcon/cateproduct.ico"},
                     {"name":"Cliente", "iconfonst":"treeviewIcon/client.ico"},
                     {"name":"Usuario", "iconfonst":"treeviewIcon/user.ico"},
                     {"name":"Producto", "iconfonst":"treeviewIcon/product.ico"},
                     {"name":"Almacen", "iconfonst":"treeviewIcon/almacen.ico"},
                     {"name":"Promotor","iconfonst":"treeviewIcon/promotore.ico"},
                     {"name":"Compra", "iconfonst":"treeviewIcon/compra.ico"},
                     {"name":"Venta", "iconfonst":"treeviewIcon/venta.ico"},
                     {"name":"Precio de producto", "iconfonst":"treeviewIcon/precio.ico"},
                     {"name":"Cerrar Session", "iconfonst":"treeviewIcon/cerrarsession.ico"}]

        for menu in enumerate(menudatos):

            item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(str(menu[1]['iconfonst'])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(0, icon)
            self.treeWidget.topLevelItem(menu[0]).setText(0, self._translate("MainWindow", str(menu[1]['name'])))

        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.treeWidget.clicked.connect(self.getValue)
    def getValue(self, ix=""):
        self.opcionSelect = ix.data()
        columnas = self.builtcolumns(self.opcionSelect)
        numcolumnas = len(columnas)
        self.token = self.login['api_token'];
        pagina = 1
        registropagina = 20

        if(self.opcionSelect == 'Dashboard'):
            self.charts()
        elif(self.opcionSelect == 'Categoria Producto'):
            datatable = self.viewcategoria.getcategorias(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Cliente'):
            datatable = self.viewcliente.getclientes(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Usuario'):
            datatable = self.viewusuario.getusurios(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Producto'):
            datatable = self.viewproducto.getproductos(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Almacen'):
            datatable = self.viewalmacen.getalmacenes(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Promotor'):
            datatable = self.viewpromotor.getpromotores(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Compra'):
            datatable = self.viewcompre.getcompras(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Venta'):
            datatable = self.viewventa.getventas(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Precio de producto'):
            datatable = self.viewprecioproduct.getproductosprecio(self.token,pagina,registropagina)
            self.table(columnas,numcolumnas,datatable,self.opcionSelect,registropagina,pagina)
        elif(self.opcionSelect == 'Cerrar Session'):
            self.close()
            self.loginview.show()
    def table(self,columnas,numcolumnas,data,type,registropagina,pagina):

        _translate = QtCore.QCoreApplication.translate
        #self.framecharts.close()
        self.frameTable = QtWidgets.QWidget(self)
        self.frameTable.setGeometry(QtCore.QRect(192, 0, 1265, 700))
        self.frameTable.setObjectName("table")
        self.frameTable.setStyleSheet("background-color: #fff")

        self.tabWidget = QtWidgets.QTabWidget(self.frameTable) # QWidget
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1265, 700))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        paginas = ['20','30','50','80','100']

        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Datos"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Nuevo"))

        btnnumpagina = QComboBox(self.tab)
        btnnumpagina.addItems(paginas)
        position = 0

        paginasfull = 1 if(data == None) else math.ceil(int(data['total'])/int(registropagina))

        for i in range(len(paginas)):
            if(paginas[i] == registropagina):
                position = i

        btnnumpagina.setCurrentIndex(position)
        btnnumpagina.activated.connect(lambda: self.changevalorpaginado(data,btnnumpagina.currentText(),type))
        btnnumpagina.setGeometry(10,10,50,30)

        pag = QLabel(self.tab)
        pag.setText('Pagina: ')
        pag.setGeometry(80, 10, 50, 30)

        self.paginatext = QSpinBox(self.tab)
        self.paginatext.setMinimum(1)
        self.paginatext.setValue(pagina)
        self.paginatext.setMaximum(paginasfull)
        self.paginatext.valueChanged.connect(lambda: self.changevalorpaginado(data,btnnumpagina.currentText(),type))
        self.paginatext.setGeometry(120,10,100,30)
        numeroregistroinsertados = 1 if(data == None) else int(data['registerpag'])
        #numeroregistroinsertados = 1 if(data == None) else int(data['data'])

        #tabla
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(0, 50, 1100, 570))
        self.tableWidget.setColumnCount(numcolumnas) # Numero de columnas
        self.tableWidget.setRowCount(numeroregistroinsertados)   #  numero de registros insertados
        self.tableWidget.setHorizontalHeaderLabels(columnas) # Nombre de las columnas
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection) #Seleccionar una sola fila a la vez
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) #  desa bilitar la edicion
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows) # seleccionar toda la fila
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.submenutable)
        item = self.tableWidget.item(10, 3)

        if(data != None):
            if type == "Categoria Producto":
                self.viewcategoria.table(self.tableWidget,data['data'])
            elif type == "Cliente":
                self.viewcliente.table(self.tableWidget,data['data'])
            elif type == "Usuario":
                self.viewusuario.table(self.tableWidget,data['data'])
            elif type == "Producto":
                self.viewproducto.table(self.tableWidget,data['data'])
            elif type == "Almacen":
                self.viewalmacen.table(self.tableWidget,data['data'])
            elif type == "Promotor":
                self.viewpromotor.table(self.tableWidget,data['data'])
            elif type == "Compra":
                self.viewcompre.table(self.tableWidget,data['data'])
            elif type == "Venta":
                self.viewventa.table(self.tableWidget,data['data'])
            elif(type == "Precio de producto"):
                self.viewprecioproduct.table(self.tableWidget,data['data'])



        if type == "Categoria Producto":

            if(self.login['type'] in ('Administrador')):
                self.viewcategoria.createview(self.token,self.tab_2)
        elif type == "Cliente":

            if(self.login['type'] in ('Administrador')):
                self.viewcliente.createview(self.token,self.tab_2)
        elif type == "Usuario":

            if(self.login['type'] in ('Administrador')):
                self.viewusuario.createview(self.token,self.tab_2)
        elif type == "Producto":

            if(self.login['type'] in ('Administrador')):
                self.viewproducto.createview(self.token,self.tab_2)
        elif type == "Almacen":
            print("Entre......")
        elif type == "Promotor":

            if (self.login['type'] in('Administrador')):
                self.viewpromotor.createview(self.token,self.tab_2)
        elif type == "Compra":

            if(self.login['type'] in('Administrador')):
                self.viewcompre.createview(self.token,self.tab_2,self.login['id'])
        elif type == "Venta":

            if(self.login['type'] in('Administrador','Vendedor')):
                self.viewventa.createview(self.token,self.tab_2,self.login['id'])

        elif type ==  'Precio de producto':
            self.viewprecioproduct.createview(self.token,self.tab_2)

        self.frameTable.show()
    def builtcolumns(self,type):
        lista = []

        if(type == "Categoria Producto"):
            lista = ["id","nombre"]
        elif(type == "Cliente"):
            lista = ["id","nombre","apellidos","telefono","direccion","cp","colonia","img"]
        elif(type == "Usuario"):
            lista = ["id","name","email","tipo user","img"]
        elif(type == "Producto"):
            lista = ["id","nombre","descripcion","precioPorKilo","img","categoria"]
        elif(type == "Almacen"):
            lista = ["id","entrada","salida","stock","usuario","producto"]
        elif(type == "Promotor"):
            lista = ["id","nombre","direccion","telefono","sitioWeb","imagen"]
        elif(type == "Compra"):
            lista = ["id","folio","cantidad_stock","precio_total","img","promotor","producto"]
        elif(type == "Venta"):
            lista = ["id","factura", "precio_total", "pago", "cliente", "usuario"]
        elif(type == "Precio de producto"):
            lista = ["id","producto","precio"]
        return lista
    def changevalorpaginado(self,data,registerpag,type):

        pagina = math.ceil(int(data['total'])/int(registerpag))

        columnas = self.builtcolumns(type)
        numcolumnas = len(columnas)
        self.token = self.login['api_token'];

        self.loadingdatarefresh(type,registerpag,self.paginatext.text())
    def loadingdatarefresh(self,type,registros,pagina):

        columnas = self.builtcolumns(self.opcionSelect)
        numcolumnas = len(columnas)

        if(type == 'Categoria Producto'):
            data = self.viewcategoria.getcategorias(self.token,pagina,registros)
            self.table(columnas,numcolumnas,data,type,registros,int(pagina))
        elif(type == 'Cliente'):
            data = self.viewcliente.getclientes(self.token,pagina,registros)
            self.table(columnas,numcolumnas,data,type,registros,int(pagina))
        elif(type == 'Usuario'):
            data = self.viewusuario.getusurios(self.token,pagina,registros)
            self.table(columnas,numcolumnas,data,type,registros,int(pagina))
        elif(type == 'Producto'):
            data = self.viewproducto.getproductos(self.token,pagina,registros)
            self.table(columnas,numcolumnas,data,type,registros,int(pagina))
        elif(type == 'Almacen'):
            data = self.viewalmacen.getalmacenes(self.token,pagina,registros)
            self.table(columnas,numcolumnas,data,type,registros,int(pagina))
        elif(type == 'Promotor'):
            data = self.viewpromotor.getpromotores(self.token,pagina,registros)
            self.table(columnas,numcolumnas,data,type,registros,int(pagina))
        elif(type == 'Compra'):
            data = self.viewcompre.getcompras(self.token,pagina,registros)
            self.table(columnas,numcolumnas,data,type,registros,int(pagina))
        elif(type == 'Venta'):
            data = self.viewventa.getventas(self.token,pagina,registros)
            self.table(columnas,numcolumnas,data,type,registros,int(pagina))

        ##print(datatable)
    def submenutable(self,position):
        indice = self.tableWidget.selectedIndexes()
        fila = [dato.text() for dato in self.tableWidget.selectedItems()]

        if(indice):
            menu = QMenu()

            # opciones para administrador
            if(self.login['type'] == 'Administrador' and self.opcionSelect in('Dashboard','Categoria Producto','Cliente','Usuario','Producto','Almacen','Promotor','Compra','Precio de producto')):
                update = menu.addAction(QIcon('icon/actualizar.ico'),"Modificar", lambda: self.modificarfilatabla(fila))
                menu.addSeparator()
            if(self.login['type'] ==  'Administrador' and self.opcionSelect in('Dashboard','Categoria Producto','Cliente','Usuario','Producto','Almacen','Promotor','Compra','Precio de producto')):
                destroyMenu = menu.addAction(QIcon('icon/destroy.ico'),"Eliminar", lambda: self.destroyfilatable(fila))
                menu.addSeparator()

            # PErmisos para vendedor
            if(self.login['type'] == 'Vendedor' and self.opcionSelect in('Categoria Producto','Producto','Compra')):
                update = menu.addAction(QIcon('icon/actualizar.ico'),"Modificar", lambda: self.modificarfilatabla(fila))
                menu.addSeparator()
            if(self.login['type'] == 'Vendedor' and self.opcionSelect in('Categoria Producto','Producto','Compra')):
                destroyMenu = menu.addAction(QIcon('icon/destroy.ico'),"Eliminar", lambda: self.destroyfilatable(fila))
                menu.addSeparator()





            menu.exec_(self.tableWidget.viewport().mapToGlobal(position))
    def modificarfilatabla(self,data):

        if(self.opcionSelect == 'Categoria Producto'):
            self.viewcategoria.edit(self.token,data)
        elif(self.opcionSelect == 'Cliente'):
            self.viewcliente.edit(self.token,data)
        elif(self.opcionSelect == 'Usuario'):
            self.viewusuario.edit(self.token,data)
        elif(self.opcionSelect == 'Producto'):
            self.viewproducto.edit(self.token,data)
        elif(self.opcionSelect == 'Almacen'):
            self.viewalmacen.edit(self.token,data)
        elif(self.opcionSelect == 'Promotor'):
            self.viewpromotor.edit(self.token,data)
        elif(self.opcionSelect == 'Compra'):
            self.viewcompre.edit(self.token,self.login['id'],data)
        elif(self.opcionSelect == 'Venta'):
            print("hola")
        elif(self.opcionSelect == 'Precio de producto'):
            self.viewprecioproduct.edit(self.token,data)
    def destroyfilatable(self,data):

        if(self.opcionSelect == 'Categoria Producto'):
            self.viewcategoria.delete(self.token,data)
        elif(self.opcionSelect == 'Cliente'):
            self.viewcliente.delete(self.token,data)
        elif(self.opcionSelect == 'Usuario'):
            self.viewusuario.delete(self.token,data,self.login['id'])
        elif(self.opcionSelect == 'Producto'):
            self.viewproducto.delete(self.token,data)
        elif(self.opcionSelect == 'Almacen'):
            print("hola")
        elif(self.opcionSelect == 'Promotor'):
            self.viewpromotor.delete(self.token,data)
        elif(self.opcionSelect == 'Compra'):
            self.viewcompre.delete(self.token,data)
        elif(self.opcionSelect == 'Venta'):
            print("hola")
        elif(self.opcionSelect == 'Precio de producto'):
            self.viewprecioproduct.delete(self.token,data)

    #reloj
    def showTime(self):

        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.label.setText(label_time)

    #evento cerrar ventana principal
    def closeEvent(self,event):
        respuesta = self.msm.messageConfirm("Salir de la aplicacion", '¿Quieres salir de la aplicacion')

        if(respuesta):
            event.accept()
            self.timer.stop()
        else:
            event.ignore()

    # Apartados de charts
    def charts(self):
        #self.loading.start()    self.resize(1300, 650)

        self.framecharts = QtWidgets.QWidget(self)
        self.framecharts.setGeometry(QtCore.QRect(192, 0, 1100, 700))
        self.framecharts.setObjectName("charts")
        self.framecharts.setStyleSheet("background-color: #fff") # red

        _translategrafig = QtCore.QCoreApplication.translate

        self.tabWidgetgrafic = QtWidgets.QTabWidget(self.framecharts) # QWidget
        self.tabWidgetgrafic.setGeometry(QtCore.QRect(0, 0, 1265, 700))
        self.tabWidgetgrafic.setObjectName("tabWidget")
        self.tabgrafic = QtWidgets.QWidget()
        self.tabgrafic.setObjectName("tab")
        self.tabWidgetgrafic.addTab(self.tabgrafic, "")
        self.tabgrafic_2 = QtWidgets.QWidget()
        self.tabgrafic_2.setObjectName("tab_2")

        paginas = ['20','30','50','80','100']

        self.tabWidgetgrafic.addTab(self.tabgrafic_2, "")
        self.tabWidgetgrafic.setTabText(self.tabWidgetgrafic.indexOf(self.tabgrafic), _translategrafig("MainWindow", "Almacen"))
        self.tabWidgetgrafic.setTabText(self.tabWidgetgrafic.indexOf(self.tabgrafic_2), _translategrafig("MainWindow", "Charts"))

        self.inexistenteproduct()
        self.graficaone()

        if(self.login['type'] in('Administrador')):
            self.graficatwo()
        self.framecharts.show()
        #self.loading.stop()

    def inexistenteproduct(self):
        # Imprimir una tabla de productos faltantes
        self.tableproductinexistencia = QtWidgets.QTableWidget(self.tabgrafic)
        self.tableproductinexistencia.setGeometry(QtCore.QRect(10, 50, 1080, 575))
        self.tableproductinexistencia.setColumnCount(2)
        self.tableproductinexistencia.setHorizontalHeaderLabels(['cantidad','nombre'])
        self.tableproductinexistencia.setAlternatingRowColors(True)
        self.tableproductinexistencia.setWordWrap(False)
        self.tableproductinexistencia.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableproductinexistencia.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableproductinexistencia.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableproductinexistencia.horizontalHeader().setStretchLastSection(True)
        self.tableproductinexistencia.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableproductinexistencia.setContextMenuPolicy(Qt.CustomContextMenu)

        self.loadingdatainexistentproduct()

        labelproductexist = QLabel("Te faltan " + str(self.productexists) + " productos en almacen",self.tabgrafic)
        labelproductexist.setGeometry(300,0,450,50)
        labelproductexist.setFont(QFont('Arial', 20))
        labelproductexist.setStyleSheet("QLabel{color:red;}")

    def graficaone(self):
        self.framechartone = QtWidgets.QWidget(self.tabgrafic_2)
        self.framechartone.setGeometry(QtCore.QRect(0, 0, 500, 300))
        self.framechartone.setObjectName("chartone")
        self.framechartone.setStyleSheet("background-color: #fff") # fondo blanco

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("Tus ventas", color="b", size="30pt")
        layout = QGridLayout()
        self.framechartone.setLayout(layout)
        layout.addWidget(self.graphWidget)

        ventaspormes = self.ctrhome.loadingventasone(self.login['api_token'],self.login['id'])
        self.ventasbymes = []
        self.meses = []
        if(ventaspormes['code'] == 200):
            datosventames = ventaspormes['data']

            self.meses = datosventames['meses']
            self.ventasbymes =  datosventames['ventas']

            pen = pg.mkPen(color=(255, 0, 0), width=4, style=QtCore.Qt.DashLine)
            self.graphWidget.plot(self.meses, self.ventasbymes, name = self.login['name'] ,pen=pen)

            self.graphWidget.setLabel('left', "<span style=\"color:red;font-size:20px\">Ventas ($)</span>")
            self.graphWidget.setLabel('bottom', "<span style=\"color:red;font-size:20px\">Mes (M)</span>")
            self.graphWidget.addLegend()

        self.framechartone.show()
    def graficatwo(self):
        self.framecharttwo = QtWidgets.QWidget(self.tabgrafic_2)
        self.framecharttwo.setGeometry(QtCore.QRect(500, 0, 500, 300))
        self.framecharttwo.setObjectName("chartone")
        self.framecharttwo.setStyleSheet("background-color: #fff") # fondo blanco

        self.graphWidgettwo = pg.PlotWidget()
        self.graphWidgettwo.setBackground('w')
        layouttwo = QGridLayout()
        self.framecharttwo.setLayout(layouttwo)
        layouttwo.addWidget(self.graphWidgettwo)

        self.graphWidgettwo.setTitle("Ventas de los usuarios", color="b", size="30pt")

        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidgettwo.setLabel("left", "Ventas ($)", **styles)
        self.graphWidgettwo.setLabel("bottom", "Mes (M)", **styles)
        self.graphWidgettwo.addLegend()
        self.graphWidgettwo.showGrid(x=True, y=True)
        self.graphWidgettwo.setXRange(0, 10, padding=0)
        self.graphWidgettwo.setYRange(20, 55, padding=0)

        ventaspormesusuarios = self.ctrhome.loadingventas(self.login['api_token'])
        meses = [2, 1, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3]

        if(ventaspormesusuarios['code'] == 200):
            datosventames = ventaspormesusuarios['data']

            for v in datosventames:
                colorR = self.generarcolorR()
                colorG = self.generarcolorG()
                colorB = self.generarcolorB()

                self.plot(meses, v['ventas'], colorR, colorG, colorB,v['name'])


        self.framecharttwo.show()
    def plot(self, x, y, colorR, colorG, colorB,usuario):

        pen = pg.mkPen(color=(colorR, colorG, colorB), width=4, style=QtCore.Qt.DashLine)
        self.graphWidgettwo.plot(x, y,pen=pen,name=usuario)

    # Genrar colores en RGB
    def generarcolorR(self):
        return random.randint(0, 255)
    def generarcolorG(self):
        return random.randint(0, 255)
    def generarcolorB(self):
        return random.randint(0, 255)

    def loadingdatainexistentproduct(self):
        datos = self.ctrhome.loadingdatosproductinexistent(self.login['api_token'])

        if(datos['code'] == 200):
            data = datos['data'];
            self.productexists = len(datos['data'])
            self.tableproductinexistencia.setRowCount(int(len(datos['data'])))

            for i,producto in enumerate(datos['data']):
                self.tableproductinexistencia.setItem(i,0,QTableWidgetItem(str(producto['stock'])))
                self.tableproductinexistencia.setItem(i,1,QTableWidgetItem(producto['nombre']))
