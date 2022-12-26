import pytest
import logging

from bin.periodo import Periodo
log = logging.getLogger(__name__)


@pytest.fixture
def periodo():
    return Periodo()


class TestPeriodo:
    @pytest.mark.parametrize(
        'ano, mes',
        [(2021, 3)]
    )
    def test_get_quinzena(self, ano, mes, periodo):
        resultado_dia = periodo.get_data(ano, mes)
        assert resultado_dia == '2-15-2021'
        log.info('Quinzena coletada com sucesso!')
