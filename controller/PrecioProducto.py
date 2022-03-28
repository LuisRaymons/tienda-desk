from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json


class PrecioProducto:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()
    def getproductosprecio(self,token,pagina,registropagina):
        url = config.APIREQUEST + "producto/precio/get"
        args = {"api_token":token,"numpag":registropagina,"pag":pagina}
        response = requests.post(url,params=args)
        data = response.json()
        return data

    def missing(self,token):
        url = config.APIREQUEST + "producto/precio/missing"
        args = {"api_token":token}
        response = requests.post(url,params=args)
        data = response.json()
        return data

    def store(self,args):
        url = config.APIREQUEST + "producto/precio/add"
        response = requests.post(url,params=args)
        data = response.json()
        return data

    def update(self,args):
        url = config.APIREQUEST + "producto/precio/update"
        response = requests.post(url,params=args)
        data = response.json()
        return data

    def delete(self,args):
        url = config.APIREQUEST + "producto/precio/delete"
        response = requests.post(url,params=args)
        data = response.json()
        return data
