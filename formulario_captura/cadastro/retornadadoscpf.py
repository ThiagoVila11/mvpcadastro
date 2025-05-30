import requests
import base64
import json
from django.conf import settings

# 1. Função para obter o token de autenticação
def get_auth_token():
        login_url = "https://api.ph3a.com.br/DataBusca/api/Account/Login"
        username = settings.API_DATABUSCA_USER
        #password = settings.API_DATABUSCA_PASS
        
        payload = {
            "UserName": username
            #"Password": password
        }
    
    # Criar autenticação básica
    #auth_string = f"{username}:{password}"
    #auth_bytes = auth_string.encode('ascii')
    #base64_auth = base64.b64encode(auth_bytes).decode('ascii')
    #headers = {
    #    "Authorization": f"Basic {base64_auth}",
    #    "Content-Type": "application/json"
    #}
        auth_string = f"{username}"
        auth_bytes = auth_string.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')
        headers = {
            "Authorization": f"Basic {base64_auth}",
            "Content-Type": "application/json"
        }
    
        response = requests.post(login_url, json=payload, headers=headers)
    
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                return response_data["data"]["Token"]
        raise Exception("Falha ao obter token de autenticação")

# 2. Função para consumir a API de dados com o token e body especificado
def get_api_data(token):
    data_url = "https://api.ph3a.com.br/DataBusca/data"
    
    # Corpo da requisição conforme especificado
    request_body = {
        "Document": "26735906845"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Token": f"{token}"            
    }
    print(headers)
    print(f"Enviando requisição para {data_url} com headers: {headers}")
            
    response = requests.post(data_url, json=request_body, headers=headers)
    print(f"Resposta: {response.status_code} - {response.text}")  
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

# Execução principal
try:
    # Obtém o token
    token = get_auth_token()
    print("Token obtido com sucesso!")
    
    # Faz a requisição aos dados com o body especificado
    api_data = get_api_data(token)
    print("\nResposta da API:")
    print(json.dumps(api_data, indent=2))
    
except Exception as e:
    print(f"Erro: {e}")