class Periodo(object):
    @staticmethod
    def get_data(ano, mes):
        """
            Retorna o dia 15 do mês anterior ao período informado
        :param ano: int
        :param mes: int
        :return:
            dados: str = '11-12-2020'
        """
        # Retorna o dia 15 do mês anterior
        return f'{mes-1}-{15}-{ano}'
