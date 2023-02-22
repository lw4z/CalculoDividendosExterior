"""
    Módulo principal com as rotas da api
"""
from datetime import datetime
from fastapi import FastAPI
from fastapi import Query
from starlette.responses import RedirectResponse

from bin.calculo_declaracao import CalculoDeclaracao
from bin.cotacao import Cotacao
from bin.periodo import Periodo

app = FastAPI(debug=True)


@app.get('/')
def get_docs():
    """Redirecionando para a tela de documentação."""
    response = RedirectResponse(url='/docs')
    return response


@app.get('/cotacao_por_dia/')
def get_cotacao_por_dia(
        ano: int,
        mes: int,
        dia: int
) -> dict:
    """Retorna a cotação da data informada."""
    data = f'{mes}-{dia}-{ano}'
    # Retorna as cotações da data informada
    result = {
        'data': datetime.strptime(data, '%m-%d-%Y'),
        'cotacao_compra': Cotacao().get_cotacao_compra(data)['cotacao'],
        'cotacao_venda': Cotacao().get_cotacao_venda(data)['cotacao']
    }
    return result


@app.get('/cotacao_busca_dia_util/')
def get_cotacao_busca_dia_util(
        ano: int,
        mes: int,
        dia: int
) -> dict:
    """Retorna a cotação buscando o último dia util anterior a data informada."""
    data = Periodo().padronizar_data(dia, mes, ano)
    # Retorna a cotação do último dia útil anterior ao dia

    return Cotacao().get_cotacao_ultimo_dia_util(data)


@app.get('/declaracao_dividendos_exterior_individual/')
async def get_declaracao_dividendos_exterior_individual(
        tipo_ativo: str = Query(alias='tipo_ativo', description='ETF ou Stock'),
        ano: int = Query(alias='ano', description='Ano em que recebeu o pagamento'),
        mes: int = Query(alias='mes', description='Mês em que recebeu o pagamento'),
        valor_bruto: float = Query(alias='valor_bruto', description='Valor bruto recebido'),
        valor_imposto: float = Query(alias='valor_imposto', description='Valor do Imposto pago'),
        codigo: str = Query(alias='codigo', description='Código do ativo individual, ex.: VOO, AAPL')
) -> dict:
    """Retorna os dados da declaração de dividendos no exterior por ticket de ativo."""
    # Gera data da primeira quinzena
    primeira_quinzena = Periodo().get_data(ano, mes)
    # Captura cotação do último dia util anterior ao dia 15
    cotacao_ultimo_dia_util = Cotacao().get_cotacao_ultimo_dia_util(primeira_quinzena)
    # Retorna o resultado dos dados para declaração dos dividendos no exterior
    resultado_declaracao = CalculoDeclaracao().calcular_declaracao_individual(
        tipo_ativo,
        codigo.upper(),
        cotacao_ultimo_dia_util['cotacao'],
        valor_bruto, valor_imposto
    )

    resultado = {
        "dia_cotacao": cotacao_ultimo_dia_util,
        "detalhes": resultado_declaracao
    }

    return resultado


@app.get('/declaracao_dividendos_exterior_mensal/')
async def get_declaracao_dividendos_exterior_mensal(
        ano: int,
        mes: int,
        valor_bruto: float,
        valor_imposto: float
) -> dict:
    """Retorna os dados da declaração de dividendos mensal no exterior."""
    # Captura segunda sexta-feira do mês anterior
    primeira_quinzena = Periodo().get_data(ano, mes)
    # Captura cotação do último dia util anterior ao dia 15
    cotacao_ultimo_dia_util = Cotacao().get_cotacao_ultimo_dia_util(primeira_quinzena)
    # Retorna o resultado dos dados para declaração dos dividendos no exterior
    resultado_declaracao = CalculoDeclaracao().calcular_declaracao_mensal(
        cotacao_ultimo_dia_util['cotacao'], valor_bruto, valor_imposto)

    resultado = {
        "dia_cotacao": cotacao_ultimo_dia_util,
        "detalhes": resultado_declaracao
    }

    return resultado

@app.get('/atualizar_base_cotacoes/')
async def atualizar_base_cotacoes() -> dict:
    """Retorna a lista de datas que foram acrescentadas na base."""
    return Cotacao().atualizar_base_cotacoes()
