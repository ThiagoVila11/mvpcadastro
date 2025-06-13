import requests
import base64
import json
from django.conf import settings

class APIDataBuscaService:
    @staticmethod
    def get_auth_token():
        login_url = "https://api.ph3a.com.br/DataBusca/api/Account/Login"
        username = settings.API_DATABUSCA_USER
        password = settings.API_DATABUSCA_PASS
        
        payload = {
            "UserName": username,
            "Password": password
        }
        
        auth_string = f"{username}"
        auth_bytes = auth_string.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')
        headers = {
            "Authorization": f"Basic {base64_auth}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(login_url, json=payload, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                print(response_data["data"]["Token"])
                return response_data["data"]["Token"]
        raise Exception("Falha ao obter token de autenticação")

    @staticmethod
    def get_api_data(cpf):
        print(f"Obtendo dados para CPF: {cpf}")
        token = APIDataBuscaService.get_auth_token()
        data_url = "https://api.ph3a.com.br/DataBusca/data"
        
        request_body = {
            "Document": cpf
            }
        
        headers = {
            "Content-Type": "application/json",
            "Token": f"{token}"            
        }
        #print(headers)
        print(f"Enviando requisição para {data_url} com headers: {headers}")
              
        response = requests.post(data_url, json=request_body, headers=headers)
        print(f"Resposta: {response.status_code} - {response.text}")      
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")