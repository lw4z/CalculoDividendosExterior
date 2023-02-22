"""
# Tela inicial
Aqui é exibida uma explicação sobre a declaração dos dividendos além da última cotação
válida e de um gráfico temporal das cotações do dolar registradas na base.
"""

import datetime
import json
import os
import pandas as pd
import requests
import streamlit as st

diretorio_atual = os.path.dirname(__file__)

# Configurações da página
st.set_page_config(
    page_title="Início",
    page_icon='🖩',
)

# Barra lateral esquerda
st.sidebar.markdown('## Configurações:')

# Botão atualizar base de dados da barra lateral
atualizar_button = st.sidebar.button('Atualizar base das cotações')

if atualizar_button:
    # Load para carregamento da atividade
    with st.spinner("Carregando..."):
        result = requests.get(
            url='http://127.0.0.1:8000/atualizar_base_cotacoes/'
        )
        if result.status_code == 200:
            st.success('Base atualizada com sucesso!')
        else:
            st.error('Ocorreu um erro durante a atualização da base!')

# Texto da tela inicial
texto = """## 🌎 Declaração de dividendos no exterior

Os impostos pagos ou retidos no exterior, para compensação no Brasil, devem ser convertidos utilizando o valor do dólar, fixado para compra pelo BACEN, do último dia útil da primeira quinzena do mês anterior ao do pagamento do imposto.

Ao receber dividendos pagos no exterior por Ações, REITs, ADRs e  ETFs é necessário apurar o carnê-leão. Trata-se de um recolhimento mensal obrigatório, pelo contribuinte, pessoa física, residente no Brasil, que receber rendimentos de outra pessoa física ou do exterior.

Para utilizar a aplicação Carnê Leão não é necessário baixar o programa ou aplicativo para celular. Acesse o Centro Virtual de Atendimento (Portal e-CAC), disponível no site da Receita Federal, selecione o serviço “Meu Imposto de Renda” > "Declarações" > "Acessar Carnê-Leão".

[Fonte](https://ajuda.bancointer.com.br/pt-BR/articles/5952518-como-faco-declaracao-de-dividendos-recebidos-no-exterior)
"""
st.markdown(texto)

# Coleta de dados para exibição da última cotação válida
data_cotacao = datetime.datetime.now()
ano = data_cotacao.year
mes = data_cotacao.strftime('%m')
dia = data_cotacao.strftime('%d')
data_get = {'ano': ano, 'mes': mes, 'dia': dia}

# Chamada da api
result = requests.get(
        url = 'http://127.0.0.1:8000/cotacao_busca_dia_util/',
        params = data_get
    )

date_str = datetime.datetime.strptime(result.json().get('data'), '%Y-%m-%dT%H:%M:%S')
date_cotacao = date_str.strftime('%d/%m/%Y')
cotacao_compra = result.json().get('cotacao_compra')
cotacao_venda = result.json().get('cotacao_venda')

# Exibição da última cotação
st.subheader(f'💲 Última cotação: **{date_cotacao}**')
if cotacao_compra > 0:
    texto = f'''
        Dólar compra: **R&#36; {cotacao_compra}**\n
        Dólar venda: **R&#36; {cotacao_venda}**'''
    st.info(texto)

# Verificando cotações por dia
st.subheader('📈 Verificando a cotação por dia')
data_cotacao = st.date_input(
    'Selecione uma data:',
    help='Selecione apenas dias úteis',
    min_value=datetime.datetime(2021, 12, 12),
    max_value=datetime.datetime.today(),
)

# Dados para a chamada da api
ano = data_cotacao.year
mes = data_cotacao.strftime('%m')
dia = data_cotacao.strftime('%d')
data_get = {'ano': ano, 'mes': mes, 'dia': dia}
cotacao_button = st.button('Pesquisar')

if cotacao_button:
    result = requests.get(
        url = 'http://127.0.0.1:8000/cotacao_por_dia/',
        params = data_get
    )
    # print(result.json().get('data'))
    date_str = datetime.datetime.strptime(result.json().get('data'), '%Y-%m-%dT%H:%M:%S')
    date = date_str.strftime('%d/%m/%Y')
    # print(data)
    cotacao_compra = result.json().get('cotacao_compra')
    cotacao_venda = result.json().get('cotacao_venda')
    if cotacao_compra > 0:
        # st.write({
        #     'data': date,
        #     'cotação compra': f'R$ {cotacao_compra}',
        #     'cotação venda': f'R$ {cotacao_venda}'
        # })
        texto = f'''
            Dia **{date}**\n
            Dólar compra: **R&#36; {cotacao_compra}**\n
            Dólar venda: **R&#36; {cotacao_venda}**'''
        st.success(texto)
    else:
        st.warning("Não há dados para esta data! Entre com uma data referente a um dia útil!")


# Carregando dados da base de cotações
path = os.path.join(diretorio_atual, '../dados/data_cotacao.json')
with open(path, 'r', encoding='utf-8') as arquivo_dados:
    cotacoes = json.load(arquivo_dados)
data_frame = pd.json_normalize(cotacoes)

# Ordenando data pela coluna data
data_frame['data'] = pd.to_datetime(data_frame['data'])
data_ordenada = data_frame.sort_values('data', ascending=False)

# Apresentando gráfico das cotações
st.subheader('📊 Histórico de cotações do dólar:', )
st.line_chart(data_ordenada, x='data', y='cotacao_compra')
