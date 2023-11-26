import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt

def create_graph_widget():
    # Lendo os dados do arquivo JSON
    with open('cotacoes_formatadas.json', 'r') as file:
        json_data = json.load(file)

    # Extraindo os dados relevantes do JSON
    dates = [datetime.utcfromtimestamp(entry['date']).strftime('%Y-%m-%d') for entry in json_data['historicalDataPrice']]
    closes = [entry['close'] for entry in json_data['historicalDataPrice']]

    # Criando o gráfico
    fig, ax = plt.subplots()
    ax.plot(dates, closes, marker='o', linestyle='-', color='b', label='Preço de Fechamento')
    ax.set_title(f'Gráfico de Linha para {json_data["longName"]}')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço de Fechamento')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()

    # Salvando o gráfico como uma imagem
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    # Criando uma instância de Image com a imagem do gráfico
    img = CoreImage(BytesIO(buffer.read()), ext='png', filename='graph.png')
    image_widget = KivyImage(texture=img.texture, size=img.size, size_hint=(None, None))

    # Criando um layout Box para conter a imagem
    graph_layout = BoxLayout()
    graph_layout.add_widget(image_widget)

    return graph_layout
