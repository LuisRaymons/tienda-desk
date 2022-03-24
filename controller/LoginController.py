from view.Errors import ErrorGeneral
from slugify import slugify
from config import env as config
import requests
import json

class LoginController:
    def __init__(self):
        self.error = ErrorGeneral.ErrorGeneral()

    def auth(self,correo,password):
        urlapi = config.APIREQUEST + "login"
        args = {"email":correo, "password":password}
        response = requests.post(urlapi,params=args)
        data = response.json()
        return data

    def store(self,args):
        url = config.APIREQUEST + "usuario/add"
        response = requests.post(url, data = args)
        data = response.json()
        return data
