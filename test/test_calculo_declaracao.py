import pytest
import logging

from bin.calculo_declaracao import CalculoDeclaracao
log = logging.getLogger(__name__)

@pytest.fixture
def calculo_declaracao():
    return CalculoDeclaracao()


class TestCalculoDeclaracao:

    @pytest.mark.parametrize(
        'codigo, cotacao, valor_bruto, valor_imposto',
        [('teste', 5.7121, 0.19, 0.06)]
    )
    def test_calculo_declaracao(
            self,
            codigo,
            cotacao,
            valor_bruto,
            valor_imposto,
            calculo_declaracao
    ):
        """Testa a funçlão de cálculo da declaração."""
        resultado = calculo_declaracao.calcular_declaracao_individual(codigo, cotacao, valor_bruto, valor_imposto)
        assert resultado['valor_bruto'] == '1.09'
        assert resultado['valor_imposto'] == '0.34'
        assert resultado['valor_liquido'] == '0.75'

        log.info('Cálculo da declaração verificada com sucesso!')
