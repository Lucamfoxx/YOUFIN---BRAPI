import json

def ler_e_imprimir_valores(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)

    for item in dados:
        print(f"Simbolo: {item['simbolo']}")
        print(f"Nome Completo: {item['nome_completo']}")
        print(f"Cotação: {item['cotacao']}")
        print(f"Preço Anterior: {item['preco_anterior']}")
        print(f"Volume: {item['volume']}")
        print("-" * 30)

# Substitua 'caminho_do_arquivo.json' pelo caminho real do seu arquivo JSON
caminho_do_arquivo = 'add.json'
ler_e_imprimir_valores(caminho_do_arquivo)
