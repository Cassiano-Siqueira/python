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
                'Mes': ['Jan', 'Jan', 'Fev', 'Fev', 'Mar', 'Mar'],
                'Categoria': ['Eletrônicos', 'Casa', 'Eletrônicos', 'Casa', 'Eletrônicos', 'Casa'],
                'ID_Pedido': [101, 102, 103, 104, 105, 106],
                'Receita': [1500.0, 900.0, 1800.0, 1100.0, 2200.0, 1350.0],
            }
        )
        caminho_arquivo = 'vendas.csv'
        dados_exemplo.to_csv(caminho_arquivo, index=False)

    df = pd.read_csv(caminho_arquivo)
    df['receita'] = pd.to_numeric(df['receita'], errors='coerce').fillna(0)
    return df


df = carregar_dados()

st.sidebar.title('Filtros')
lista_de_categorias = sorted(df['Categoria'].dropna().unique().tolist())
categorias_selecionadas = st.sidebar.multiselect(
    'Selecione as Categorias',
    options=lista_de_categorias,
    default=lista_de_categorias,
)

if categorias_selecionadas:
    df_filtrado = df[df['Categoria'].isin(categorias_selecionadas)].copy()
else:
    df_filtrado = df.copy()

col1, col2 = st.columns(2)
receita_calculada = df_filtrado['Receita'].sum()
total_pedidos = df_filtrado['ID_Pedido'].count()

with col1:
    st.metric(label='Receita Total', value=receita_calculada)

with col2:
    st.metric(label='Total de Pedidos', value=total_pedidos)

aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])

with aba1:
    dados_agrupados = df_filtrado.groupby('Mes', as_index=False)['receita'].sum()
    st.area_chart(dados_agrupados.set_index('Mes')['receita'])

with aba2:
    st.dataframe(df_filtrado)
    st.download_button(
        label='Baixar CSV',
        data=df_filtrado.to_csv(index=False),
        file_name='recorte.csv',
        mime='text/csv',
    )
