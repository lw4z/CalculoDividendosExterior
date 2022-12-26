import pytest
import logging

from bin.calculo_declaracao import CalculoDeclaracao
from bin.cotacao import Cotacao
from bin.periodo import Periodo
log = logging.getLogger(__name__)


@pytest.fixture
def periodo():
    return Periodo()


@pytest.fixture
def cotacao():
    return Cotacao()


@pytest.fixture
def calculo():
    return CalculoDeclaracao()


class TestDeclaracaoDividendosExterior:
    @pytest.mark.parametrize(
        'ano, mes, valor_bruto, valor_imposto',
        [(2022, 11, 0.19, 0.06)]
    )
    def test_get_declaracao_dividendos_exterior(
            self,
            ano,
            mes,
            valor_bruto,
            valor_imposto,
            periodo,
            cotacao,
            calculo
    ):
        """Verifica o funcionamento do fluxo da declaração."""
        primeira_quinzena = periodo.get_data(ano, mes)
        cotacao_ultimo_dia_util = cotacao.get_cotacao_ultimo_dia_util(primeira_quinzena)
        resultado_declaracao = calculo.calcular_declaracao_mensal(
            cotacao_ultimo_dia_util['cotacao'], valor_bruto, valor_imposto)
        log.info(str(resultado_declaracao))
