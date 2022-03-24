import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from win10toast import ToastNotifier

class ErrorGeneral(QDialog): # self.setWindowIcon(QIcon('icon/tienda.png'))

	def messageError(self,Titulo,Mensaje):
		 msgBox = QMessageBox()
		 msgBox.setIcon(QMessageBox.Warning)  # Question Information Warning Critical
		 msgBox.setWindowIcon(QIcon('icon/tienda.png'))
		 msgBox.setText(Mensaje)
		 msgBox.setWindowTitle(Titulo)
		 msgBox.addButton(str("Aceptar"), QMessageBox.ActionRole)
		 #msgBox.setStandardButtons(QMessageBox.Ok)
		 msgBox.exec()
	def messageConfirm(self,Titulo,Mensaje):
		msm = QMessageBox()
		msm.setIcon(QMessageBox.Question)
		msm.setWindowIcon(QIcon('icon/tienda.png'))
		msm.setWindowTitle(Titulo)
		msm.setText(Mensaje)
		msm.addButton(str("Aceptar"), QMessageBox.ActionRole)
		msm.addButton(str("Cancelar"), QMessageBox.RejectRole)
		val=msm.exec()
		if(val == 0):
			return True
		elif(val == 1):
			return False
	def messageInfo(self,titulo,mensaje):
		msInfo = QMessageBox()
		msInfo.setIcon(QMessageBox.Information)
		msInfo.setWindowIcon(QIcon('icon/tienda.png'))
		msInfo.setWindowTitle(titulo)
		msInfo.setText(mensaje)
		msInfo.addButton(str("Aceptar"), QMessageBox.ActionRole)
		#msInfo.setStandardButtons(QMessageBox.Ok)
		msInfo.exec()
	def messageToast(self,titulo,mensaje):
		toast = ToastNotifier()
		#toast.setWindowIcon(QIcon('icon/tienda.png'))
		toast.show_toast(titulo,mensaje,duration=1) # duracion de un segundo
	def messagewhatsapp(self):
		value, ok = QInputDialog.getText(self, "getText()", "Mensaje")
		if ok and value != '' : print('Nombre:', value)
