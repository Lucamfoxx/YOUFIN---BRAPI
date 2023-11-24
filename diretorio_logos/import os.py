import os
import subprocess

# Pasta onde estão os arquivos SVG
diretorio_svg = '.'

# Pasta onde serão salvos os arquivos PNG
diretorio_png = 'diretorio_logos_png'

# Certifique-se de que o diretório para armazenar os PNGs existe, se não, crie-o
if not os.path.exists(diretorio_png):
    os.makedirs(diretorio_png)

# Caminho para o executável do Inkscape
inkscape_path = 'D:/PROGRAMAS/inkscape/bin/inkscape.exe'

# Listar todos os arquivos na pasta SVG
arquivos_svg = [arquivo for arquivo in os.listdir(diretorio_svg) if arquivo.endswith('.svg')]

# Iterar sobre os arquivos SVG e converter para PNG
for arquivo_svg in arquivos_svg:
    caminho_svg = os.path.join(diretorio_svg, arquivo_svg)
    nome_arquivo = os.path.splitext(arquivo_svg)[0]  # Remover a extensão .svg
    caminho_png = os.path.join(diretorio_png, f'{nome_arquivo}.png')

    try:
        # Comando para converter SVG para PNG usando Inkscape
        comando = f'"{inkscape_path}" --export-type=png --export-filename={caminho_png} "{caminho_svg}"'
        subprocess.run(comando, shell=True, check=True)
        print(f"Conversão bem-sucedida: {arquivo_svg} convertido para {nome_arquivo}.png")
    except subprocess.CalledProcessError as e:
        print(f"Falha ao converter {arquivo_svg} para PNG. Erro: {e}")
