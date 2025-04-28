import requests
import base64

# URL da API
url = "https://api.ph3a.com.br/DataBusca/api/Account/Login"

# Credenciais de autenticação básica
username = "dev@reda.one"
password = "REDA@#$%Summer22"

# Dados do corpo da requisição
payload = {
    "UserName": username,
    "Password": password
}

# Criar o header de autenticação básica
auth_string = f"{username}:{password}"
auth_bytes = auth_string.encode('ascii')
base64_auth = base64.b64encode(auth_bytes).decode('ascii')
headers = {
    "Authorization": f"Basic {base64_auth}",
    "Content-Type": "application/json"
}

# Fazer a requisição POST
response = requests.post(url, json=payload, headers=headers)


# Verificar a resposta
if response.status_code == 200:
    response_data = response.json()
    token = response_data["data"]["Token"]
    print(token)
    print("Requisição bem-sucedida!")
    print("Resposta:", response.json())
    print(response.json())
else:
    print(f"Erro na requisição. Código de status: {response.status_code}")
    print("Resposta:", response.text)


