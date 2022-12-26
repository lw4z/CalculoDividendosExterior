"""
    Fonte dos dados:
    https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/
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
        data_atual_pesquisa = date.today().strftime('%m-%d-%Y')

        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r', encoding='utf-8') as arquivo_dados:
            cotacoes = json.load(arquivo_dados)
        data_frame = pd.json_normalize(cotacoes)

        # Ordenando data pela coluna data e coletando a data mais atual nos data
        data_frame['data'] = pd.to_datetime(data_frame['data'])
        data_ordenada = data_frame.sort_values('data', ascending=False)['data'].head(1)
        ultima_data = data_ordenada.iloc[0]
        ultima_data = ultima_data.strftime('%m-%d-%Y')

        dict_result = []

        if data_atual_pesquisa != ultima_data:
            data_atual = datetime.strptime(data_atual_pesquisa, '%m-%d-%Y')
            while True:
                if self.get_base_cotacao(data_atual_pesquisa) == {}:
                    pass
                dia_anterior = data_atual - timedelta(days=1)
                dia_anterior = dia_anterior.strftime('%m-%d-%Y')
                data_atual = datetime.strptime(dia_anterior, '%m-%d-%Y')
                cotacao = self.get_base_cotacao(dia_anterior)
                if cotacao != {} and cotacao['data'] != ultima_data:
                    log.info(f'Importando dados do dia: {cotacao["data"]}')
                    dict_result.append(cotacao)
                if cotacao != {} and cotacao['data'] == ultima_data:
                    break

        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r+', encoding='utf-8') as arquivo_dados:
            data_file = json.load(arquivo_dados)
            for item in dict_result:
                data_file.append(item)
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

        if len(data_result['value']) > 0:
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
        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r', encoding='utf-8') as arquivo_dados:
            cotacoes = json.load(arquivo_dados)
        data_frame = pd.json_normalize(cotacoes)

        # Procurando os dados de arcodo com a data
        data_result = data_frame.loc[(data_frame['data'] == data)]

        # Capturando o valor da cotação
        cotacao_periodo = 0
        if len(data_result['cotacao_compra']) > 0:
            cotacao_periodo = data_result['cotacao_compra'].values[0]

        log.info('Criando dicionário com dados da cotação.')
        resultado = {
            'data': datetime.strptime(data, '%m-%d-%Y'),
            'cotacao': cotacao_periodo,
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
        resultado_cotacao = 0

        if self.get_cotacao_compra(data)['cotacao'] == 0:
            while resultado_cotacao == 0:
                # if resultado_cotacao is not None:
                #     break
                dia_anterior = dia_util_inicial - timedelta(days=1)
                dia_anterior = dia_anterior.strftime('%m-%d-%Y')
                dia_util_inicial = datetime.strptime(dia_anterior, '%m-%d-%Y')
                resultado_cotacao = self.get_cotacao_compra(dia_anterior)[
                    'cotacao'
                ]
                print(dia_anterior)
                print(resultado_cotacao)
        else:
            resultado_cotacao = self.get_cotacao_compra(data)['cotacao']

        log.info('Criando dicionário com dados da cotação.')
        resultado = {
            'data': datetime.strptime(data, '%m-%d-%Y'),
            'cotacao': resultado_cotacao,
        }

        return resultado
