import json
import logging
import os

import pandas as pd
import pytest

from bin.cotacao import Cotacao

diretorio_atual = os.path.dirname(__file__)
log = logging.getLogger(__name__)


@pytest.fixture
def cotacao():
    return Cotacao()


class TestCotacao:
    @pytest.mark.parametrize(
        'data',
        ['12-15-2021']
    )
    def test_get_cotacao(
            self,
            data,
            cotacao
    ):
        """Verifica uma cotação específica"""
        resultado = cotacao.get_cotacao_compra(data)
        assert resultado['cotacao'] == 5.7121
        log.info('Cotação verificada com sucesso!')

    @pytest.mark.parametrize(
        'data',
        ['12-05-2021']
    )
    def test_get_cotacao_procura_dia_util(
            self,
            data,
            cotacao
    ):
        """Verifica a cotação buscando o último dia útil anterior a data informada."""
        resultado = cotacao.get_cotacao_ultimo_dia_util(data)
        assert resultado['cotacao'] == 5.6426
        log.info('Cotação por último dia útil verificada com sucesso!')

    @pytest.mark.skip
    def test_atualizar_base_cotacoes(
            self,
            cotacao
    ):
        """Testa a atualização da base de dados das cotações."""
        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r', encoding='utf-8') as arquivo_dados:
            cotacoes = json.load(arquivo_dados)
        df_antes = pd.json_normalize(cotacoes)

        cotacao.atualizar_base_cotacoes()

        path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
        with open(path, 'r', encoding='utf-8') as arquivo_dados:
            cotacoes = json.load(arquivo_dados)
        df_depois = pd.json_normalize(cotacoes)

        assert len(df_depois) > len(df_antes)

        log.info('Atualização da base de dados verificada com sucesso!')
