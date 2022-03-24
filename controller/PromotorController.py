from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json

class PromotorController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()
    def getpromotores(self,token,pagina,registropagina):
        url = config.APIREQUEST + "promotor/get"
        args = {"api_token":token,"numpag":registropagina,"pag":pagina}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def store(self,datos,file):
        url = config.APIREQUEST + "promotor/add"
        response = requests.post(url, data = datos, files = file)
        data = response.json()
        return data
    def update(self,datos,file):
        url = config.APIREQUEST + "promotor/update"
        response = requests.post(url, data = datos, files = file)
        data = response.json()
        return data
    def delete(self,token,id):
        url = config.APIREQUEST + "promotor/delete"
        args = {"api_token":token,"id":id}
        response = requests.post(url, params=args)
        data = response.json()
        return data
