import datetime
import requests
import re
import streamlit as st

st.set_page_config(
    page_title="Cotação do último dia útil",
    page_icon='📆',
)

st.header('📅 Cálculo da declaração individual')
st.markdown('##### Indique os dividendos recebidos por um ativo')

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
tipo_ativo = st.radio('Selecione o tipo de ativo:',
                      ('ETF', 'Stock'),
                      help='Escolha o tipo de ativo do qual você recebeu os dividendos',
                      horizontal=True)

# Definindo colunas para as entradas de dados
col1, col2 = st.columns(2)
with col1:
    codigo_ativo = st.text_input('Digite o código do ativo: *', help='ETF, Stock, etc.', placeholder='ex.: VOO')
    data_cotacao = st.date_input(
        'Selecione a data do pagamento: *',
        help='Selecione a data em que recebeu os dividendos',
        min_value=datetime.datetime(2021, 12, 12),
        max_value=datetime.datetime.today(),
    )
with col2:
    valor_bruto = st.number_input('Digite o valor bruto dos dividendos recebidos: *',
                                  help='O valor bruto é aquele que você recebe em dólares indicado pela sua corretora',
                                  min_value=0.0)
    valor_imposto = st.number_input('Digite o valor do imposto pago: *',
                              help='O valor do imposto é aquele que é abatido após o valor bruto, '
                                   'esse valor também é indicado pela sua corretora',
                                min_value=0.0)

# Dados para a chamada da api
ano = data_cotacao.year
mes = data_cotacao.strftime('%m')
data_get = {
    'tipo_ativo': tipo_ativo,
    'ano': ano,
    'mes': mes,
    'valor_bruto': valor_bruto,
    'valor_imposto': valor_imposto,
    'codigo': codigo_ativo
}
cotacao_button = st.button('Calcular')

if cotacao_button:
    if tipo_ativo and ano and mes and valor_bruto and valor_imposto and codigo_ativo:
        result = requests.get(
            url = 'http://127.0.0.1:8000/declaracao_dividendos_exterior_individual/',
            params = data_get
        )
        print(result.text)

        date_str = datetime.datetime.strptime(result.json().get('dia_cotacao')['data'], '%Y-%m-%dT%H:%M:%S')
        date = date_str.strftime('%d/%m/%Y')

        st.markdown('**Detalhes:**')
        texto1 = f'''
            Último dia útil da primeira quinzena do mês anterior: **{date}**\n
            Cotação do dia: **R$ {result.json().get('detalhes')['cotacao_periodo']}**\n
            Valor bruto recebido: **{result.json().get('detalhes')['valor_bruto_reais']}**\n
            Valor do imposto pago: **{result.json().get('detalhes')['valor_imposto_reais']}**\n
            Valor líquido recebido: **{result.json().get('detalhes')['valor_liquido_reais']}**
        '''
        st.warning(texto1)

        st.markdown('**Modelo de mensagem de rendimentos para o Carnê Leão:**')

        mensagem_rendimentos = re.sub(r'[$]', r'\$', result.json().get('detalhes')['rendimentos_mensagem_exemplo'])
        st.success(mensagem_rendimentos)
        st.info(f'''Valor a ser declarado **{result.json().get('detalhes')['valor_bruto_reais']}**''')
        st.markdown('**Modelo de mensagem de pagamento de imposto para o Carnê Leão:**')
        mensagem_imposto = re.sub(r'[$]', r'\$', result.json().get('detalhes')['pagamentos_mensagem_exemplo'])
        st.success(mensagem_imposto)
        st.info(f'''Valor a ser declarado **{result.json().get('detalhes')['valor_imposto_reais']}**''')
    else:
        st.warning("Por favor, preencha todos os campos para prosseguir!")