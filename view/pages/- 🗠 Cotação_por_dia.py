import datetime
import requests
import streamlit as st

st.set_page_config(
    page_title="Cotação por dia",
    page_icon=":chart_with_upwards_trend:",
)


st.header('📈 Verificando a cotação por dia')

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
        st.write({
            'data': date,
            'cotação compra': f'R$ {cotacao_compra}',
            'cotação venda': f'R$ {cotacao_venda}'
        })
        texto = f'''
            Dia **{date}**\n
            Cotação do dolar de compra: **R&#36; {cotacao_compra}**\n
            Cotação do dolar de venda: **R&#36; {cotacao_venda}**'''
        st.success(texto)
    else:
        st.warning("Não há dados para esta data! Entre com uma data referente a um dia útil!")



