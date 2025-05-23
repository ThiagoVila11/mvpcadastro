import requests    
from django.contrib import messages
from django.shortcuts import render, redirect

def Api_Lexio(request):
    print('Inicio da api')
    response = requests.post(
        #'http://3.143.172.37:8001/api/login/',
        'https://app.lexio.legal/api/generate_form_document_v2/Vila11LocacaoQuadroResumoTeste',
        json={ "signature_list": [
                {
                    "service": "lexiosign",
                    "titulo": "Pre-Contrato_teste", 
                    "signers": [
                        {
                            "nome": "Nome Signatário 1",
                            "email": "signatario1@email.com",
                            "funcao": "Representante Legal"
                        },
                        {
                            "nome": "Nome Signatário 2", 
                            "email": "signatario2@email.com",
                            "funcao": "Testemunha" 
                        }
                    ],
                    "send_email": True,
                    "order_by": False, 
                    "lembrete": 3,
                    "engine_campos": {
                        "Landlord": "Lexio Tecnologia Ltda", 
                        "Type": "Sociedade de responsabilidade limitada", 
                        "Cnpj": "32.772.921/0001-69", 
                        "AddressLandlord": "R. dos Pinheiros, 498 - cj. 42 - Pinheiros, São Paulo - SP, 05422-902", 
                        "IndicatedPerson": "Maria da Silva Pereira", 
                        "EmailPerson": "maria.pereira@vila11.com.br", 
                        "Lessee": "1", 
                        "NameOne": "José Eduardo dos Santos", 
                        "ProfessionOne": "advogado", 
                        "MaritalStatOne": "casado em regime de comunhão parcial de bens", 
                        "RgOne": "12.345.678-9", 
                        "CpfOne": "123.456.789-10", 
                        "EmailOne": "jose.edu@gmail.com", 
                        "CelOne": "(11) 99999-9999", 
                        "AddressOne": "Avenida Paulista, n.1000, apt 404, Bela Vista, São Paulo/SP, CEP 01234-567", 
                        "NameTwo": "", 
                        "ProfessionTwo": "", 
                        "MaritalStatTwo": "", 
                        "RgTwo": "", 
                        "CpfTwo": "", 
                        "EmailTwo": "", 
                        "CelTwo": "", 
                        "AddressTwo": "", 
                        "NameThree": "", 
                        "ProfessionThree": "", 
                        "MaritalStatThree": "", 
                        "RgThree": "", 
                        "CpfThree": "", 
                        "EmailThree": "", 
                        "CelThree": "", 
                        "AddressThree": "", 
                        "NameFour": "", 
                        "ProfessionFour": "", 
                        "MaritalStatFour": "", 
                        "RgFour": "", 
                        "CpfFour": "", 
                        "EmailFour": "", 
                        "CelFour": "", 
                        "AddressFour": "", 
                        "NameFive": "", 
                        "ProfessionFive": "", 
                        "MaritalStatFive": "", 
                        "RgFive": "", 
                        "CpfFive": "", 
                        "EmailFive": "", 
                        "CelFive": "", 
                        "AddressFive": "", 
                        "Residents": "1", 
                        "ResNameOne": "João Pedro Batista", 
                        "ResRgOne": "98.765.432-1", 
                        "ResCpfOne": "987.654.321-10", 
                        "ResNameTwo": "", 
                        "ResRgTwo": "", 
                        "ResCpfTwo": "", 
                        "ResNameThree": "", 
                        "ResRgThree": "", 
                        "ResCpfThree": "", 
                        "ResNameFour": "", 
                        "ResRgFour": "", 
                        "ResCpfFour": "", 
                        "AdmName": "Administradora XPTO Ltda", 
                        "AdmCnpj": "98.765.432/0001-11", 
                        "AdmCel": "(11) 99999-9999", 
                        "Apartment": "404", 
                        "CondoName": "Condomínio XPTO", 
                        "Registration": "123456789", 
                        "ContactCondo": "(11) 99999-9999", 
                        "CnpjCondo": "65.432.158/0001-11", 
                        "PropertyAddress": "Avenida Brigadeiro Faria Lima, n. 404, apt 44, Vila Olímpia, São Paulo/SP, CEP 04321-987", 
                        "Iptu": "123456789", 
                        "RentMonth": "3000,00", 
                        "DataBase": "20250601", 
                        "DataSig": "20250523", 
                        "WitName1": "Fulano da Silva", 
                        "WitAdress1": "Rua Vergueiro, n. 404, Paraíso, São Paulo/SP, CEP 01586-025", 
                        "WitRg1": "65.432.147-9", 
                        "WitName2": "", 
                        "WitAdress2": "", 
                        "WitRg2": "", 
                    }
                }
            ]
        },
        headers={'Content-Type': 'application/json',
                 "Authorization": "Bearer 8e3d3c2bc7bce9c379e4976c4de696e7a73eb1888f6d19182c3741269fcb6b7e"},
        timeout=10
    )
    print(response)
    if response.status_code != 200:
        print('status diferente de 200')
        print(response.status_code)
        messages.error(request, 'Credenciais inválidas')
        return render(request, 'registration/login.html')
        
    token_data = response.json()
    print(token_data)
    return render(request, 'registration/login.html')

