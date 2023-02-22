"""
    Fonte dos dados:
    https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/
    O formato da data utilizado na base é mês-dia-ano.
"""
import json
import logging
import os
from datetime import date, datetime, timedelta

import pandas as pd
import requests

diretorio_atual = os.path.dirname(__file__)
log = logging.getLogger(__name__)


class Cotacao:
    """
    Classe responsável pela coleta e manipulação dos dados das cotações.
    Métodos:
        atualizar_base_cotacoes -> verifica os dados salvos e atualiza.
        get_base_cotacoes -> faz a busca pelos dados no site do banco central.
        get_cotacao_compra -> retorna a cotação de compra da data especificada.
        get_cotacao_ultimo_dia_util -> retorna a cotação do último dia útil anterior a data informada.
    """
    def atualizar_base_cotacoes(self):
        """Verifica a última data do json de dados e atualiza as cotações até a última atual."""
        # Convertendo a data de hoje para string
        data_atual_pesquisa = date.today().strftime('%m-%d-%Y')

        # Abrindo arquivo de dados das cotações em um dataframe
        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r', encoding='utf-8') as arquivo_dados:
            cotacoes = json.load(arquivo_dados)
        data_frame = pd.json_normalize(cotacoes)

        # Ordenando data pela coluna data e coletando a data mais atual nos dados
        data_frame['data'] = pd.to_datetime(data_frame['data'])
        data_ordenada = data_frame.sort_values('data', ascending=False)['data'].head(1)
        primeira_data_ordenada = data_ordenada.iloc[0]
        ultima_data = primeira_data_ordenada.strftime('%m-%d-%Y')

        dict_result = []

        if data_atual_pesquisa != ultima_data:
            data_atual = datetime.strptime(data_atual_pesquisa, '%m-%d-%Y')
            while True:
                if self.get_base_cotacao(data_atual_pesquisa) == {}:
                    pass
                # Subtrair um dia do último dia util da base
                dia_anterior = data_atual - timedelta(days=1)
                # Convertendo o formato de data para string
                dia_anterior = dia_anterior.strftime('%m-%d-%Y')
                # Convertendo o formato de string para data
                data_atual = datetime.strptime(dia_anterior, '%m-%d-%Y')
                # Coletando cotação do dia anterior
                cotacao = self.get_base_cotacao(dia_anterior)
                # Verificando se a cotação é nula e se é diferente da última data válida
                if cotacao != {} and cotacao['data'] != ultima_data:
                    log.info(f'Importando dados do dia: {cotacao["data"]}')
                    dict_result.append(cotacao)
                # Verificando se a cotação é nula e se é igual ao dia atual
                if cotacao != {} and cotacao['data'] == ultima_data:
                    break

        # Adicionando os novos dados coletados na base de dados das cotações
        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r+', encoding='utf-8') as arquivo_dados:
            data_file = json.load(arquivo_dados)
            [data_file.append(item) for item in dict_result]
            arquivo_dados.seek(0)
            json.dump(data_file, arquivo_dados)

        return dict_result

    @staticmethod
    def get_base_cotacao(data):
        """
        Coleta os dados da base Olinda do banco central.
        :param data: string
        :return:
            {
                data: string
                cotacao_compra: float
                cotacao_venda: float
            }
        """
        url = (
            f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo('
            f'dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)'
            f'?@dataInicial=%27{data}%27&@dataFinalCotacao=%27{data}%27'
        )
        log.info('Acessando base do Banco central.')
        response = requests.get(url, timeout=30)
        data_result = response.json()
        cotacao = {}

        # Verificando se houve retorno da data especificada
        if len(data_result['value']) > 0:
            # Criando dicionário com os resultados
            for cotacao in data_result['value']:
                date_time = datetime.strptime(
                    cotacao['dataHoraCotacao'], '%Y-%m-%d %H:%M:%S.%f'
                )
                data = str(date_time.strftime('%m-%d-%Y'))
                cotacao_compra = cotacao['cotacaoCompra']
                cotacao_venda = cotacao['cotacaoVenda']

                cotacao = {
                    'data': data,
                    'cotacao_compra': cotacao_compra,
                    'cotacao_venda': cotacao_venda,
                }

        return cotacao

    @staticmethod
    def get_cotacao_compra(data):
        """
            Retorna a cotação a partir da data informada.
        :param data: string
        :return:
            {
                'data': datetime,
                'cotacao': dict
            }
        """
        # Abrindo arquivo de dados das cotações
        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r', encoding='utf-8') as arquivo_dados:
            cotacoes = json.load(arquivo_dados)
        data_frame = pd.json_normalize(cotacoes)

        # Procurando os dados de arcodo com a data
        data_result = data_frame.loc[(data_frame['data'] == data)]

        # Capturando o valor da cotação de compra
        cotacao_periodo = 0
        if len(data_result['cotacao_compra']) > 0:
            cotacao_periodo = data_result['cotacao_compra'].values[0]

        log.info('Criando dicionário com dados da cotação de compra.')
        resultado = {
            'data': datetime.strptime(data, '%m-%d-%Y'),
            'cotacao': cotacao_periodo
        }

        return resultado

    @staticmethod
    def get_cotacao_venda(data):
        """
            Retorna a cotação a partir da data informada.
        :param data: string
        :return:
            {
                'data': datetime,
                'cotacao': dict
            }
        """
        # Abrindo arquivo de dados das cotações
        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r', encoding='utf-8') as arquivo_dados:
            cotacoes = json.load(arquivo_dados)
        data_frame = pd.json_normalize(cotacoes)

        # Procurando os dados de arcodo com a data
        data_result = data_frame.loc[(data_frame['data'] == data)]

        # Capturando o valor da cotação de venda
        cotacao_periodo = 0
        if len(data_result['cotacao_venda']) > 0:
            cotacao_periodo = data_result['cotacao_venda'].values[0]

        log.info('Criando dicionário com dados da cotação de venda.')
        resultado = {
            'data': datetime.strptime(data, '%m-%d-%Y'),
            'cotacao': cotacao_periodo
        }

        return resultado

    def get_cotacao_ultimo_dia_util(self, data):
        """
            Retorna a data e a cotação do último dia útil anterior a segunda sexta-feira do mês anterior.
        :param data: string
        :return:
            {
                'data': datetime,
                'cotacao': dict
            }
        """
        dia_util_inicial = datetime.strptime(data, '%m-%d-%Y')
        dia_anterior = dia_util_inicial.strftime('%m-%d-%Y')
        resultado_cotacao_compra = 0
        resultado_cotacao_venda = 0

        # Verificando se há cotação na data especificada
        if self.get_cotacao_compra(data)['cotacao'] == 0:
            while resultado_cotacao_compra == 0:
                # Subtrair um dia do último dia util da base
                dia_anterior = dia_util_inicial - timedelta(days=1)
                # Convertendo o formato da data
                dia_anterior = dia_anterior.strftime('%m-%d-%Y')
                # Colocando o dia anterior no topo da pilha
                dia_util_inicial = datetime.strptime(dia_anterior, '%m-%d-%Y')
                # Coletando cotação do dia anterior
                resultado_cotacao_compra = self.get_cotacao_compra(dia_anterior)['cotacao']
                resultado_cotacao_venda = self.get_cotacao_venda(dia_anterior)['cotacao']
        else:
            resultado_cotacao_compra = self.get_cotacao_compra(data)['cotacao']
            resultado_cotacao_venda = self.get_cotacao_venda(data)['cotacao']

        log.info('Criando dicionário com dados da cotação.')
        resultado = {
            'data': datetime.strptime(dia_anterior, '%m-%d-%Y'),
            'cotacao_compra': resultado_cotacao_compra,
            'cotacao_venda': resultado_cotacao_venda,
        }

        return resultado
