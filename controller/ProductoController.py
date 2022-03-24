from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json


class ProductoController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()
    def getproductos(self,token,pagina,registropagina):
        url = config.APIREQUEST + "producto/get"
        args = {"api_token":token,"numpag":registropagina,"pag":pagina}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def loadingcategorias(self,token):
        url = config.APIREQUEST + "categoria/producto/get/all"
        args = {"api_token": token}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def store(self,datos,file):
        url = config.APIREQUEST + "producto/add"
        response = requests.post(url, data = datos, files = file)
        data = response.json()
        return data
    def update(self,datos,file):
        url = config.APIREQUEST + "producto/update"
        response = requests.post(url, data = datos, files = file)
        data = response.json()
        return data
    def delete(self,token,id):
        url = config.APIREQUEST + "producto/delete"
        args = {"api_token": token, "id":id}
        response = requests.post(url, params = args)
        data = response.json()
        return data
