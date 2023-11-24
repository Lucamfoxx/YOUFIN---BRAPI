import requests
import os
import json

def obter_cotacao_e_logo(codigo_empresa, token):
    # Construir a URL com o endpoint de cotação para um ticker específico
    url_cotacao = f"https://brapi.dev/api/quote/{codigo_empresa}?token={token}"

    # Fazer a solicitação HTTP para obter dados da empresa
    response = requests.get(url_cotacao)

    # Verificar o código de status da resposta
    if response.status_code == 200:
        # Se a solicitação foi bem-sucedida, obter a URL do logo
        dados = response.json()
        logo_url = dados['results'][0]['logourl']

        # Baixar a logo da empresa
        baixar_logo(logo_url, codigo_empresa)
    else:
        # Se houve um erro na solicitação, imprimir a mensagem de erro
        erro = response.json()
        print(f"Erro na solicitação para {codigo_empresa}: {erro['message']}")

def baixar_logo(logo_url, codigo_empresa):
    # Certifique-se de que o diretório para armazenar as logos existe, se não, crie-o
    diretorio_logos = 'diretorio_logos'
    if not os.path.exists(diretorio_logos):
        os.makedirs(diretorio_logos)

    # Obter o conteúdo do SVG
    logo_response = requests.get(logo_url)

    # Verificar o código de status da resposta
    if logo_response.status_code == 200:
        # Salvar o conteúdo do SVG em um arquivo no diretório de logos com o nome do código da empresa
        with open(os.path.join(diretorio_logos, f"{codigo_empresa}.svg"), 'w', encoding='utf-8') as f:
            f.write(logo_response.text)
        print(f"Logo de {codigo_empresa} baixado com sucesso.")
    else:
        print(f"Falha ao baixar o logo de {codigo_empresa}. Status Code: {logo_response.status_code}")

# Substitua 'seu_token_aqui' pelo seu token de autenticação real
token = '4Rgd828GN7h8cLkUrxP1gK'

# Carregar o JSON com os códigos das empresas
caminho_json_empresas = 'empresas.json'
with open(caminho_json_empresas, 'r', encoding='utf-8') as f:
    dados_empresas = json.load(f)

# Iterar sobre as empresas e obter cotação e logo
for codigo_empresa in dados_empresas:
    obter_cotacao_e_logo(codigo_empresa, token)
