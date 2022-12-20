from fastapi import FastAPI
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
        mes: str,
        dia: int
):
    """Retorna a cotação da data informada."""
    data = f'{mes}-{dia}-{ano}'
    # Retorna a cotação da data informada
    return Cotacao().get_cotacao_compra(data)


@app.get('/cotacao_busca_dia_util/')
def get_cotacao_busca_dia_util(
        ano: int,
        mes: str,
        dia: int
):
    """Retorna a cotação buscando o último dia util anterior a data informada."""
    data = f'{mes}-{dia}-{ano}'
    # Retorna a cotação do último dia útil anterior ao dia
    return Cotacao().get_cotacao_ultimo_dia_util(data)


@app.get('/declaracao_dividendos_exterior_individual/')
async def get_declaracao_dividendos_exterior_individual(
        ano: int,
        mes: int,
        valor_bruto: float,
        valor_imposto: float,
        codigo: str
):
    """Retorna os dados da declaração de dividendos no exterior."""
    # Gera data da primeira quinzena
    primeira_quinzena = Periodo().get_data(ano, mes)
    # Captura cotação do último dia util anterior ao dia 15
    cotacao_ultimo_dia_util = Cotacao().get_cotacao_ultimo_dia_util(primeira_quinzena)
    # Retorna o resultado dos dados para declaração dos dividendos no exterior
    resultado_declaracao = CalculoDeclaracao().calcular_declaracao_individual(
        codigo, cotacao_ultimo_dia_util['cotacao'], valor_bruto, valor_imposto)

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
):
    """Retorna os dados da declaração de dividendos no exterior."""
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
