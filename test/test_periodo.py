import pytest

from bin.periodo import Periodo


@pytest.fixture
def periodo():
    return Periodo()


class TestPeriodo:
    @pytest.mark.parametrize(
        'ano, mes',
        [(2021, 3)]
    )
    def test_get_sexta_segunda_semana(self, ano, mes, periodo):
        resultado_dia = periodo.get_data(ano, mes)
        assert resultado_dia == '2-15-2021'
