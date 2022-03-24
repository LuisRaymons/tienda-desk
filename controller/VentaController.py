from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json

class VentaController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()
    def getventas(self,token,pagina,registropagina):
        url = config.APIREQUEST + "venta/get"
        args = {"api_token":token,"numpag":registropagina,"pag":pagina}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def loadingcliente(self,token):
        url = config.APIREQUEST + "cliente/get/all"
        args = {"api_token":token}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def loadingproductos(self,token):
        url = config.APIREQUEST + "producto/get/all"
        args = {"api_token":token}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def loadingpagos(self):
        url = config.APIREQUEST + "get/pago"
        response = requests.get(url)
        data = response.json()
        return data
    def searchproduct(self,token,product):
        url = config.APIREQUEST + "producto/get/name"
        args = {"api_token":token,"name":product}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def searchprecoproducto(self,token,id):
        url = config.APIREQUEST + "producto/precio/get/one"
        args = {"api_token":token,"id":id}
        response = requests.post(url,params=args)
        data = response.json()
        return data

    def store(self,datos):
        url = config.APIREQUEST + "venta/add"
        response = requests.post(url,params=datos)
        response.headers['content-type']
        response.encoding
        data = response.json()
        print("------------------datos enviados---------------------------")
        print(data['request'])
        return data
