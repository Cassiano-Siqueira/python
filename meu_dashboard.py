import os

import pandas as pd
import streamlit as st

st.title('Dashboard de Vendas')


@st.cache_data
def carregar_dados():
    arquivos_possiveis = ['vendas.csv', 'vendas_brasil.csv']
    caminho_arquivo = next((arquivo for arquivo in arquivos_possiveis if os.path.exists(arquivo)), None)

    if caminho_arquivo is None:
        dados_exemplo = pd.DataFrame(
            {
                'mes': ['Jan', 'Jan', 'Fev', 'Fev', 'Mar', 'Mar'],
                'categoria': ['Eletrônicos', 'Casa', 'Eletrônicos', 'Casa', 'Eletrônicos', 'Casa'],
                'id_pedido': [101, 102, 103, 104, 105, 106],
                'receita': [1500.0, 900.0, 1800.0, 1100.0, 2200.0, 1350.0],
            }
        )
        caminho_arquivo = 'vendas.csv'
        dados_exemplo.to_csv(caminho_arquivo, index=False)

    df = pd.read_csv(caminho_arquivo)

    colunas = {coluna.lower(): coluna for coluna in df.columns}

    coluna_mes = next((colunas[key] for key in ['mes', 'month', 'data', 'date'] if key in colunas), None)
    coluna_categoria = next((colunas[key] for key in ['categoria', 'category', 'categorias'] if key in colunas), None)
    coluna_receita = next((colunas[key] for key in ['receita', 'valor', 'total', 'total_receita'] if key in colunas), None)
    coluna_pedido = next((colunas[key] for key in ['id_pedido', 'pedido', 'order_id', 'id'] if key in colunas), None)

    if coluna_mes is not None:
        df['mes'] = pd.to_datetime(df[coluna_mes], errors='coerce').dt.to_period('M').astype(str)
    else:
        df['mes'] = 'Sem mês'

    if coluna_categoria is not None:
        df['categoria'] = df[coluna_categoria]
    else:
        df['categoria'] = 'Sem categoria'

    if coluna_receita is not None:
        df['receita'] = pd.to_numeric(df[coluna_receita], errors='coerce').fillna(0)
    else:
        df['receita'] = 0

    if coluna_pedido is not None:
        df['id_pedido'] = df[coluna_pedido]
    else:
        df['id_pedido'] = range(1, len(df) + 1)

    return df


df = carregar_dados()

st.sidebar.title('Filtros')
lista_de_categorias = sorted(df['categoria'].dropna().unique().tolist())
categorias_selecionadas = st.sidebar.multiselect(
    'Selecione as Categorias',
    options=lista_de_categorias,
    default=lista_de_categorias,
)

if categorias_selecionadas:
    df_filtrado = df[df['categoria'].isin(categorias_selecionadas)].copy()
else:
    df_filtrado = df.copy()

col1, col2 = st.columns(2)
receita_calculada = df_filtrado['receita'].sum()
total_pedidos = df_filtrado['id_pedido'].count()

with col1:
    st.metric(label='Receita Total', value=receita_calculada)

with col2:
    st.metric(label='Total de Pedidos', value=total_pedidos)

aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])

with aba1:
    dados_agrupados = df_filtrado.groupby('mes', as_index=False)['receita'].sum()
    st.area_chart(dados_agrupados.set_index('mes')['receita'])

with aba2:
    st.dataframe(df_filtrado)
    st.download_button(
        label='Baixar CSV',
        data=df_filtrado.to_csv(index=False),
        file_name='recorte.csv',
        mime='text/csv',
    )
