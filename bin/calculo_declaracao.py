import locale


class CalculoDeclaracao(object):
    @staticmethod
    def calcular_declaracao_mensal(
            cotacao,
            valor_bruto,
            valor_imposto
    ):
        """Realizar o cálculo da declaração para dados menais."""
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        recebido_reais = valor_bruto * float(cotacao)
        pago_reais = valor_imposto * cotacao
        valor_liquido = recebido_reais - pago_reais

        # Dados convertidos para formato monetário
        cotacao_real = str(cotacao).replace('.', ',')
        valor_bruto_dolar = locale.currency(valor_bruto, symbol=False)
        valor_imposto_dolar = locale.currency(valor_imposto, symbol=False)
        valor_recebido_reais = locale.currency(
            valor_bruto * float(cotacao), symbol=False
        )
        importo_pago_reais = locale.currency(
            valor_imposto * cotacao, symbol=False
        )
        valor_liquido_reais = locale.currency(valor_liquido, symbol=False)
        resultado_calculo = {
            'cotacao_periodo': cotacao,
            'valor_bruto': f'{recebido_reais:.2f}',
            'valor_imposto': f'{pago_reais:.2f}',
            'valor_liquido': f'{valor_liquido:.2f}',
            'redimentos_mensagem_exemplo': f'Dividendos recebidos no valor de US$ {valor_bruto_dolar} '
            f'com cotação do dolar R$ {cotacao_real} ',
            'pagamentos_mensagem_exemplo': f'Imposto pago no exterior sobre os dividendos '
            f'no valor de US$ {valor_imposto_dolar} '
            f'com cotação do dolar R$ {cotacao_real}',
            'valor_bruto_reais': f'R$ {valor_recebido_reais}',
            'valor_imposto_reais': f'R$ {importo_pago_reais}',
            'valor_liquido_reais': f'R$ {valor_liquido_reais}',
        }

        return resultado_calculo

    @staticmethod
    def calcular_declaracao_individual(
            codigo,
            cotacao,
            valor_bruto,
            valor_imposto
    ):
        """Retorna as informações da declaração individual incluindo o campo de código para informar um único ativo."""
        calculo_mensal = CalculoDeclaracao().calcular_declaracao_mensal(
            cotacao, valor_bruto, valor_imposto
        )

        # Dados convertidos para formato monetário
        cotacao_real = str(cotacao).replace('.', ',')
        valor_bruto_dolar = locale.currency(valor_bruto, symbol=False)
        valor_imposto_dolar = locale.currency(valor_imposto, symbol=False)

        # Construção do dicionário com os valores para o resultado
        resultado_calculo = {
            'cotacao_periodo': cotacao,
            'valor_bruto': calculo_mensal['valor_bruto'],
            'valor_imposto': calculo_mensal['valor_imposto'],
            'valor_liquido': calculo_mensal['valor_liquido'],
            'redimentos_mensagem_exemplo': f'Dividendos recebidos do ETF {codigo} no valor de US$ {valor_bruto_dolar} '
            f'com cotação do dólar R$ {cotacao_real}',
            'pagamentos_mensagem_exemplo': f'Imposto pago no exterior sobre os dividendos do ETF {codigo} '
            f'no valor de US$ {valor_imposto_dolar} '
            f'com cotação do dólar R$ {cotacao_real}',
            'valor_bruto_reais': calculo_mensal['valor_bruto_reais'],
            'valor_imposto_reais': calculo_mensal['valor_imposto_reais'],
            'valor_liquido_reais': calculo_mensal['valor_liquido_reais'],
        }

        return resultado_calculo
