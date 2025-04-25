from PIL import Image
import pytesseract
import cv2
import re
# Configuração para Windows (descomente se necessário)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def processar_cnh_texto_bruto(caminho_imagem):
    # 1. Carregar e pré-processar a imagem
    img = cv2.imread(caminho_imagem)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # 2. Extrair todo o texto da imagem
    texto = pytesseract.image_to_string(thresh, lang='por')
    print("Texto Bruto: " + texto)
    
    # 3. Processar o texto para extrair campos específicos
    dados = extrair_campos_cnh(texto)
    
    # 4. Exibir resultados
    print("\n=== DADOS DA CNH EXTRAÍDOS ===")
    for campo, valor in dados.items():
        print(f"{campo.replace('_', ' ').title()}: {valor}")

def extrair_campos_cnh(texto):
    campos = {
        'nome': None,
        'cpf': None,
        'rg': None
    }
    
    # Padrões de expressão regular para cada campo
    padroes = {
        'nome': r'(?:NOME|NOME COMPLETO)[:\s]*([A-ZÀ-Ü\s]+)\n',
        'cpf': r'(?:CPF)[:\s]*([0-9]{4git checkout main})',
        #'cpf': r'(?:CPF)[:\s]*([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2})',
        'rg': r'(?:RG|IDENTIDADE | DOC. IDENTIDADE)[:\s]*([0-9\.\-–—/]+[A-Za-z]?)'
    }
    
    # Buscar cada campo usando os padrões
    for campo, padrao in padroes.items():
        print('Padroes: ' + padrao)
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            campos[campo] = match.group(1).strip()
    
    print(campos['cpf'])
    # Pós-processamento específico
    if campos['nome']:
        campos['nome'] = re.sub(r'\s+', ' ', campos['nome']).strip()
    
    if campos['cpf']:
        # Formatar CPF padrão (000.000.000-00)
        cpf_numeros = re.sub(r'[^0-9]', '', campos['cpf'])
        campos['cpf'] = f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
    
    return campos

# Exemplo de uso
processar_cnh_texto_bruto('C:\Projetos\minhacnh.jpg')