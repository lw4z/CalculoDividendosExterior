"""
    O cálculo da declaração é baseado na cotação do último dia útil da primeira quinzena do mês anterior ao recebimento
    dos dividendos.
    O formato da data utilizado na base é mês-dia-ano.
"""
class Periodo:
    """Classe responsável por repassar a primeira quinzena do mês anterior."""
    @staticmethod
    def get_data(
            ano: int,
            mes: int
    ) -> str:
        """
            Retorna o dia 15 do mês anterior ao período informado. Esse retorno é baseado na
            necessidade para o cálculo da declaração, ou seja, "o último dia útil da primeira
            quinzena do mês anterior".
        :param ano: int
        :param mes: int
        :return:
            dados: str = '11-15-2020'
        """
        # Retorna o dia 15 do mês anterior
        return f'{mes-1}-{15}-{ano}'

    @staticmethod
    def padronizar_data(
            dia: int,
            mes: str,
            ano: int
    ) -> str:
        """Retorna a data em um formato padrinizado de acordo com a base de origem dos dados."""
        return f'{mes}-{dia}-{ano}'