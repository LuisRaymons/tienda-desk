import pymysql
from config import env


class Conexion:

	def conexion(self):
		try:
			#self.connection = pymysql.connect( host='localhost', user='root', password='', db='tiendavirtual')
			self.connection = pymysql.connect(host=env.HOST,user=env.USER,password=env.PASSWORD,db=env.DB)
			self.cursor = self.connection.cursor()
			self.valores =("success", 200,self.connection,self.cursor)
		except Exception as e:
			self.valores =("error",500)
		return self.valores
	def closeconexion(self):
			self.connection.close()
			self.cursor.close()
