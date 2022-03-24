from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json


class ClienteController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()
    def getclientes(self,token,pagina,registropagina):
        url = config.APIREQUEST + "cliente/get"
        args = {"api_token":token,"numpag":registropagina,"pag":pagina}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def store(self,datos,files):

        url = config.APIREQUEST + "cliente/add"
        response = requests.post(url, data = datos, files = files)
        data = response.json()
        return data

    def update(self,datos,files):

        url = config.APIREQUEST + "cliente/update"
        response = requests.post(url, data = datos, files = files)
        data = response.json()
        return data

    def delete(self,token,id):

        url = config.APIREQUEST + "cliente/delete"
        args = {"api_token":token,"id":id}
        response = requests.post(url, params = args)
        data = response.json()
        return data
