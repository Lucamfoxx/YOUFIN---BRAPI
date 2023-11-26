import os
import matplotlib
import threading
import json
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO


from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
import kivymd
import requests

token = '4Rgd828GN7h8cLkUrxP1gK'


# Ajustando o tamanho da janela
Window.size = (460, 720)

# Carregando automaticamente o arquivo KV correspondente
Builder.load_file("telas.kv")

# Definindo a classe da tela de SplashScreen
class SplashScreen(Screen):
    
    pass

# Definindo a classe da tela SecondScreen
class SecondScreen(Screen):
    def update_data(self, dados_empresa):
        # Atualizar os widgets com os dados obtidos
        self.ids.simbolo_label.text = f"{dados_empresa['simbolo']}"
        self.ids.nome_label.text = f"{dados_empresa['nome_completo']}"
        self.ids.cotacao_label.text = f"R$ {dados_empresa['cotacao']}"
        self.ids.preco_anterior_label.text = f"Preço Anterior: R$ {dados_empresa['preco_anterior']}"
        self.ids.volume_label.text = f"Volume: {dados_empresa['volume']}"

        # Carregar a imagem diretamente do diretorio_logos
        logo_path = os.path.join('diretorio_logos', f"{dados_empresa['simbolo']}.png")
        self.ids.logo_image.source = logo_path
    
class ThirdScreen(Screen):
    pass


# Definindo a classe principal da aplicação
class HealthApp(MDApp):
    def build(self):
        # Criando o gerenciador de telas
        self.sm = ScreenManager()
        
        # Adicionando as telas ao gerenciador
        self.splash_screen = SplashScreen(name='splash')
        self.second_screen = SecondScreen(name='second')
        self.sm.add_widget(self.splash_screen)
        self.sm.add_widget(self.second_screen)
        self.third_screen = ThirdScreen(name='third')
        self.sm.add_widget(self.third_screen)

        # Retorne o gerenciador de telas como interface da aplicação
        return self.sm
        
        # Retornando o gerenciador de telas como interface da aplicação
    
    def favoritos(self):
        self.sm.current = 'third'
        self.load_favorites()

    def load_favorites(self):
        try:
            with open('add.json', 'r', encoding='utf-8') as file:
                favorites_data = json.load(file)
        except FileNotFoundError:
            print("Erro: O arquivo 'add.json' não foi encontrado.")
            return

        # Limpar a lista existente na ThirdScreen
        self.third_screen.ids.lista_layout.clear_widgets()

        # Adicionar dados dos favoritos à ThirdScreen
        for favorite in favorites_data:
            # Crie um BoxLayout para cada favorito
            box_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
            
            # Adicione Labels para exibir apenas os valores de cada favorito
            for value in favorite.values():
                label = Label(text=f"{value}")
                box_layout.add_widget(label)

            # Adicione o BoxLayout à lista_layout
            self.third_screen.ids.lista_layout.add_widget(box_layout)

    def botao_add_clicado(self):
    # Adicione a lógica que deseja executar quando o botão for clicado
        dados_empresa = {
            "simbolo": self.second_screen.ids.simbolo_label.text,
            "nome_completo": self.second_screen.ids.nome_label.text,
            "cotacao": self.second_screen.ids.cotacao_label.text,
            "preco_anterior": self.second_screen.ids.preco_anterior_label.text,
            "volume": self.second_screen.ids.volume_label.text,
        }

        if dados_empresa:
            self.salvar_json(dados_empresa)
            print("Informações salvas no arquivo add.json!")

    def salvar_json(self, dados_empresa):
        # Salva as informações em um arquivo JSON
        arquivo_json = "add.json"
        try:
            with open(arquivo_json, "r", encoding="utf-8") as file:
                # Carrega o conteúdo atual do arquivo se existir
                data = json.load(file)
        except FileNotFoundError:
            # Cria um novo arquivo se não existir
            data = []

        # Adiciona os novos dados à lista
        data.append(dados_empresa)

        # Salva a lista no arquivo JSON
        with open(arquivo_json, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        
    def on_start(self):
        # Inicia a tarefa demorada em um thread secundário
        threading.Thread(target=self.perform_background_task).start()

        # Verifica se o arquivo de fonte existe antes de usá-lo
        font_path = "Poppins-SemiBold.ttf"
        if not os.path.exists(font_path):
            print(f"Erro: O arquivo de fonte '{font_path}' não foi encontrado.")
            return

    def perform_background_task(self):
        # Adicione sua lógica de tarefa de segundo plano aqui
        print("Background task is running.")

    def search_company(self, query):
        # Carregue o JSON
        try:
            with open('empresas.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Erro: O arquivo 'empresas.json' não foi encontrado.")
            return

        # Pesquise a empresa pelo nome ou código
        result = None
        for code, name in data.items():
            if query.lower() in name.lower() or query.lower() in code.lower():
                result = {"codigo": code, "nome": name}
                break

        if result:
            dados_empresa = self.obter_cotacao(result['codigo'])

            if dados_empresa:
                historico = os.path.join(os.path.dirname(__file__), "historico")
                
                # Construindo o caminho completo para o arquivo na pasta "historico"
                caminho = os.path.join(historico, f"{result['codigo']}.json")

                # Acessar a segunda tela e atualizar os widgets com os dados obtidos
                self.sm.current = 'second'
                self.second_screen.update_data(dados_empresa)
                self.obter_cotacoes_por_dia(result['codigo'])
                self.create_graph_widget(caminho)
    def obter_cotacao(self, code):
        # Construir a URL com o endpoint de cotação para um ticker específico
        url = f"https://brapi.dev/api/quote/{code}?token=4Rgd828GN7h8cLkUrxP1gK"

        # Fazer a solicitação HTTP
        response = requests.get(url)

        # Verificar o código de status da resposta
        if response.status_code == 200:
            # Se a solicitação foi bem-sucedida, imprimir a cotação se disponível
            dados = response.json()

            # Extração de dados
            cotacao = dados['results'][0]['regularMarketPrice']
            simbolo = dados['results'][0]['symbol']
            nome_completo = dados['results'][0]['longName']
            preco_anterior = dados['results'][0]['regularMarketPreviousClose']
            volume = dados['results'][0]['regularMarketVolume']

            # Imprimir dados
            print(f"Codigo: {simbolo}")
            print(f"Nome Completo: {nome_completo}")
            print(f"Cotação: {cotacao}")
            print(f"Preço Anterior: {preco_anterior}")
            print(f"Volume: {volume}")

            # Retornar os dados
            return {
                "simbolo": simbolo,
                "nome_completo": nome_completo,
                "cotacao": cotacao,
                "preco_anterior": preco_anterior,
                "volume": volume,
            }
        else:
            # Se houve um erro na solicitação, imprimir a mensagem de erro
            erro = response.json()
            print(f"Erro na solicitação: {erro['message']}")
            return None

    def obter_cotacoes_por_dia(self, ticker):
        # Construir o caminho da pasta "historico"
        historico_folder = os.path.join(os.path.dirname(__file__), "historico")

        # Verificar se a pasta "historico" existe, caso contrário, criar
        if not os.path.exists(historico_folder):
            os.makedirs(historico_folder)

        # Construir o caminho completo para o arquivo na pasta "historico"
        nome_arquivo = os.path.join(historico_folder, f"{ticker}.json")

        # Construir a URL com o endpoint para obter as informações por dia
        url = f"https://brapi.dev/api/quote/{ticker}?range=3mo&interval=1d&token=4Rgd828GN7h8cLkUrxP1gK"

        try:
            # Fazer a solicitação HTTP
            response = requests.get(url)

            # Verificar o código de status da resposta
            print(f"Código de status: {response.status_code}")

            # Verificar se a solicitação foi bem-sucedida
            response.raise_for_status()

            # Obter os dados de cotação
            dados_cotacao = response.json().get('results', [])

            if dados_cotacao:
                dados_formatados = {
                    'longName': dados_cotacao[0]['longName'],
                    'symbol': dados_cotacao[0]['symbol'],
                    'historicalDataPrice': dados_cotacao[0]['historicalDataPrice']
                }

                # Construa o caminho completo para o arquivo na pasta "historico"
                caminho = os.path.join(historico_folder, f"{ticker}.json")

                with open(caminho, 'w', encoding='utf-8') as json_file:
                    json.dump(dados_formatados, json_file, ensure_ascii=False, indent=4)
                    print(f"Dados formatados e salvos com sucesso em '{caminho}'.")
                
            else:
                print(f"Falha ao obter as cotações dos últimos 3 meses para {ticker}.")
        
        except requests.exceptions.HTTPError as errh:
            print(f"Erro HTTP: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Erro de conexão: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout na solicitação: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Erro na solicitação: {err}")
            
    def create_graph_widget(self, caminho):
        with open(caminho, 'r') as file:
            json_data = json.load(file)
        

        dates = [datetime.utcfromtimestamp(entry['date']).strftime('%Y-%m-%d') for entry in json_data['historicalDataPrice']]
        closes = [entry['close'] for entry in json_data['historicalDataPrice']]

        fig, ax = plt.subplots()
        ax.plot(dates, closes, marker='o', linestyle='-', color='b', label='Preço de Fechamento')
        ax.set_title(f'Gráfico de Linha para {json_data["longName"]}')
        ax.set_xlabel('Data')
        ax.set_ylabel('Preço de Fechamento')
        ax.tick_params(axis='x', rotation=45)
        ax.legend()

        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)

        img = CoreImage(BytesIO(buffer.read()), ext='png', filename='graph.png')
        image_widget = KivyImage(texture=img.texture, size=img.size, size_hint=(None, None))

        # Adicione o widget do gráfico diretamente ao graph_layout
        self.second_screen.ids.graph_layout.add_widget(image_widget)


# Verifica se o código está sendo executado diretamente
if __name__ == "__main__":
    HealthApp().run()
    
