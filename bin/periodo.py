"""
    O cálculo da declaração é baseado na cotação do último dia útil da primeira quinzena do mês anterior ao recebimento
    dos dividendos.
"""
class Periodo:
    """Classe responsável por repassar a primeira quinzena do mês anterior."""
    @staticmethod
    def get_data(
            ano,
            mes
    ):
        """
            Retorna o dia 15 do mês anterior ao período informado.
        :param ano: int
        :param mes: int
        :return:
            dados: str = '11-12-2020'
        """
        # Retorna o dia 15 do mês anterior
        return f'{mes-1}-{15}-{ano}'
