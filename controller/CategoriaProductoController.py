from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json

class CategoriaProductoController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()

    def getcategorias(self,token,pagina,registropagina):
        url = config.APIREQUEST + "categoria/producto/get"
        args = {"api_token":token,"numpag":registropagina,"pag":pagina}
        response = requests.post(url,params=args)
        data = response.json()
        return data
    def store(self,nombre,token):
        url = config.APIREQUEST + "categoria/producto/add"
        args = {"api_token":token,"nombre":nombre}
        response = requests.post(url,params=args)
        data = response.json()
        return data;
    def update(self,token,id,nombre):
        url = config.APIREQUEST + "categoria/producto/update"
        args = {"api_token":token,"id":id,"nombre":nombre}
        response = requests.post(url,params=args)
        data = response.json()
        return data;

    def delete(self,token,id):
        url = config.APIREQUEST + "categoria/producto/delete"
        args = {"api_token":token,"id":id}
        response = requests.post(url,params=args)
        data = response.json()
        return data;
