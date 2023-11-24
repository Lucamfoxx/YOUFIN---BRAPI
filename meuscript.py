from deep_translator import GoogleTranslator
import requests
import json

def translate_to_pt(description):
    try:
        translated_text = GoogleTranslator(source='en', target='pt').translate(description)
        return translated_text
    except Exception as e:
        print(f"Erro ao traduzir: {str(e)}")
        return description

# Carregar dados do JSON
with open('empresas.json', 'r', encoding='utf-8') as json_file:
    empresas = json.load(json_file)

# Dicionário para armazenar as informações
empresas_info = {}

# Iterar sobre as empresas
for codigo, nome_empresa in empresas.items():
    try:
        url = f"https://brapi.dev/api/quote/{codigo}"
        params = {
            'modules': 'summaryProfile',
            'token': '4Rgd828GN7h8cLkUrxP1gK',  # Substitua pelo seu token
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            try:
                summary_profile = data['results'][0]['summaryProfile']
                # Traduzir diretamente para o português
                translated_description = translate_to_pt(summary_profile['longBusinessSummary'])

                # Adicionar informações ao dicionário
                empresas_info[codigo] = {
                    'Nome': data['results'][0]['longName'],
                    'Setor': summary_profile.get('sectorDisp', ''),
                    'Indústria': summary_profile.get('industryDisp', ''),
                    'Site': summary_profile.get('website', ''),
                    'Telefone': summary_profile.get('phone', ''),
                    'Endereço': summary_profile.get('address1', ''),
                    'Cidade': summary_profile.get('city', ''),
                    'Estado': summary_profile.get('state', ''),
                    'País': summary_profile.get('country', ''),
                    'Descrição da Empresa (Traduzida)': translated_description,
                }
            except KeyError as e:
                print(f"Erro ao processar os dados para {nome_empresa}: {str(e)}")
        else:
            print(f"Requisição para {nome_empresa} falhou com código de status {response.status_code}")

    except Exception as e:
        print(f"Erro ao processar os dados para {nome_empresa}: {str(e)}")

# Salvar dicionário em um arquivo JSON
with open('empresas_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(empresas_info, json_file, ensure_ascii=False, indent=4)
