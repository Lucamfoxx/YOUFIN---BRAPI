import os
import threading
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
import json
import requests

# Ajustando o tamanho da janela
Window.size = (350, 580)

# Carregando automaticamente o arquivo KV correspondente
Builder.load_file("telas.kv")

# Definindo a classe da tela de SplashScreen
class SplashScreen(Screen):
    pass

# Definindo a classe da tela SecondScreen
class SecondScreen(Screen):
    def update_data(self, dados_empresa):
        # Atualizar os widgets com os dados obtidos
        self.ids.simbolo_label.text = f"CODIGO: {dados_empresa['simbolo']}"
        self.ids.nome_label.text = f"Nome Completo: {dados_empresa['nome_completo']}"
        self.ids.cotacao_label.text = f"Cotação: R$ {dados_empresa['cotacao']}"
        self.ids.preco_anterior_label.text = f"Preço Anterior: R$ {dados_empresa['preco_anterior']}"
        self.ids.volume_label.text = f"Volume: {dados_empresa['volume']}"

        # Carregar a imagem diretamente do diretorio_logos
        logo_path = os.path.join('diretorio_logos', f"{dados_empresa['simbolo']}.png")
        self.ids.logo_image.source = logo_path

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
        
        # Retornando o gerenciador de telas como interface da aplicação
        return self.sm

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
                # Acessar a segunda tela e atualizar os widgets com os dados obtidos
                self.sm.current = 'second'
                self.second_screen.update_data(dados_empresa)

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

# Verifica se o código está sendo executado diretamente
if __name__ == "__main__":
    HealthApp().run()