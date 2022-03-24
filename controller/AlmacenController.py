from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json

class AlmacenController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()

    def getalmacenes(self,token,pagina,registropagina):
        url = config.APIREQUEST + "almacen/get"
        args = {"api_token":token,"numpag":registropagina,"pag":pagina}
        response = requests.post(url,params=args)
        data = response.json()
        return data


    def update(self,datos):

        url = config.APIREQUEST + "almacen/update"
        response = requests.post(url, data = datos)
        data = response.json()
        return data
