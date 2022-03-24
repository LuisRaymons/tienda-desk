from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json


class HomeController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()

    def searchcolonias(self,cp,token):

        url = config.APIREQUEST + "codigo/postal"
        args = {"api_token":token,"CP":cp}
        response = requests.post(url,params=args)
        data = response.json()
        return data

    def loadingventas(self,token):
        url = config.APIREQUEST + "venta/total/mes"
        args = {"api_token":token}
        response = requests.post(url,params=args)
        data = response.json()
        return data

    def loadingventasone(self,token,id):
        url = config.APIREQUEST + "venta/total/mes/" + str(id)
        args = {"api_token":token}
        response = requests.post(url,params=args)
        data = response.json()
        return data
