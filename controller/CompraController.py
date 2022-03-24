from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json


class CompraController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()
    def getcompras(self,token,pagina,registropagina):
        url = config.APIREQUEST + "compra/get"
        args = {"api_token":token,"numpag":registropagina,"pag":pagina}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def loadingproducts(self,token):
        url = config.APIREQUEST + "producto/get/all"
        args = {"api_token": token}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def loadingpromotor(self,token):
        url = config.APIREQUEST + "promotor/get/all"
        args = {"api_token": token}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def store(self,datos,file):
        url = config.APIREQUEST + "compra/add"
        response = requests.post(url, data = datos, files = file)
        data = response.json()
        return data

    def update(self,datos,file):
        url = config.APIREQUEST + "compra/update"
        response = requests.post(url, data = datos, files = file)
        data = response.json()
        return data

    def delete(self,token,id):
        url = config.APIREQUEST + "compra/delete"
        args = {"api_token":token,"id":id}
        response = requests.post(url, params = args)
        data = response.json()
        return data
