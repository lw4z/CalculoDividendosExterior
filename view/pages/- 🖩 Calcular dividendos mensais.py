import datetime
import requests
import re
import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Cotação do último dia útil",
    page_icon='🗓️',
)
st.header('🗓️ Cálculo da declaração mensal️')

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

# Entradas de informações
data_cotacao = st.date_input(
    'Selecione o mês do pagamento: *',
    help='Selecione qualquer data do em que recebeu os dividendos',
    min_value=datetime.datetime(2021, 12, 12),
    max_value=datetime.datetime.today(),
)

col1, col2 = st.columns(2)
with col1:
    valor_bruto = st.number_input('Digite o valor bruto dos dividendos recebidos: *',
                            help='O valor bruto é aquele que você recebe em dólares indicado pela sua corretora',
                              min_value=0.0)
with col2:
    valor_imposto = st.number_input('Digite o valor do imposto pago: *',
                              help='O valor do imposto é aquele que é abatido após o valor bruto, '
                                   'esse valor também é indicado pela sua corretora',
                                min_value=0.0)

# Dados para a chamada da api
ano = data_cotacao.year
mes = data_cotacao.strftime('%m')
data_get = {
    'ano': ano,
    'mes': mes,
    'valor_bruto': valor_bruto,
    'valor_imposto': valor_imposto,
}
cotacao_button = st.button('Calcular')

if cotacao_button:
    if ano and mes and valor_bruto and valor_imposto:
        result = requests.get(
            url = 'http://127.0.0.1:8000/declaracao_dividendos_exterior_mensal/',
            params = data_get
        )
        print(result.text)

        date_str = datetime.datetime.strptime(result.json().get('dia_cotacao')['data'], '%Y-%m-%dT%H:%M:%S')
        date = date_str.strftime('%d/%m/%Y')

        st.text('Detalhes:')
        texto1 = f'''
            Cotação obtida do dia: **{date}**\n
            Valor bruto recebido: **{result.json().get('detalhes')['valor_bruto_reais']}**\n
            Valor do imposto pago: **{result.json().get('detalhes')['valor_imposto_reais']}**\n
            Valor líquido recebido: **{result.json().get('detalhes')['valor_liquido_reais']}**
        '''
        st.warning(texto1)

        st.text('Modelo de mensagem de rendimentos:')
        mensagem_rendimentos = re.sub(r'[$]', r'\$', result.json().get('detalhes')['rendimentos_mensagem_exemplo'])
        st.success(mensagem_rendimentos)

        st.text('Modelo de mensagem de pagamento de imposto:')
        mensagem_imposto = re.sub(r'[$]', r'\$', result.json().get('detalhes')['pagamentos_mensagem_exemplo'])
        st.success(mensagem_imposto)
    else:
        st.warning("Por favor, preencha todos os campos para prosseguir!")
