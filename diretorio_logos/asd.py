from PIL import Image
import os

def redimensionar_imagens_na_pasta(fator):
    # Criar a pasta 'png_grand' se não existir
    pasta_saida = 'png_grand'
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Obter a lista de arquivos na pasta atual
    arquivos_na_pasta = os.listdir()

    # Filtrar apenas os arquivos PNG
    arquivos_png = [arquivo for arquivo in arquivos_na_pasta if arquivo.lower().endswith(".png")]

    # Iterar sobre cada arquivo PNG e redimensioná-lo
    for nome_arquivo in arquivos_png:
        # Abrir a imagem
        imagem = Image.open(nome_arquivo)

        # Obter as dimensões originais
        largura_original, altura_original = imagem.size

        # Calcular as novas dimensões
        nova_largura = largura_original * fator
        nova_altura = altura_original * fator

        # Redimensionar a imagem
        imagem_redimensionada = imagem.resize((nova_largura, nova_altura))

        # Salvar a nova imagem na pasta 'png_grand'
        caminho_saida = os.path.join(pasta_saida, nome_arquivo)
        imagem_redimensionada.save(caminho_saida)

        print(f"Imagem {nome_arquivo} redimensionada com sucesso. Salva em {pasta_saida}.")

# Fator de redimensionamento (10x maior)
fator_redimensionamento = 10

# Chamar a função para redimensionar todas as imagens PNG na pasta
redimensionar_imagens_na_pasta(fator_redimensionamento)
