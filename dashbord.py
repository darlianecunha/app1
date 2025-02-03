import streamlit as st
import pandas as pd

# Definir estilo global com fundo branco e títulos azul escuro
st.markdown(
    """
    <style>
        body {
            background-color: white;
            color: black;
        }
        h1, h2 {
            color: #003366;
        }
        .stDataFrame, .stTable {
            background-color: white;
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho do Dashboard
st.markdown("<h1 style='text-align: center; color: #003366;'>Dashboard de Exportações por País e Produto (2023)</h1>", unsafe_allow_html=True)

# Carregar os dados
@st.cache_data
def load_data():
    file_path = "data.xlsx"
    df = pd.read_excel(file_path)
    df = df.rename(columns={
        'Ano': 'ano',
        'Nomenclatura Simplificada': 'tipo_produto',
        'Total de Movimentação Portuária\nem toneladas (t)': 'movimentacao_total_t',
        'País Origem': 'pais'
    })
    df = df[df["ano"] == 2023]  # Filtrar apenas para 2023
    return df

df = load_data()

# Calcular total geral para percentual
total_movimentacao_geral = df["movimentacao_total_t"].sum()

# Agregar por país e produto
resumo = df.groupby(["pais", "tipo_produto"], as_index=False)["movimentacao_total_t"].sum()
resumo_total_pais = df.groupby("pais", as_index=False)["movimentacao_total_t"].sum()
resumo_total_pais["percentual"] = (resumo_total_pais["movimentacao_total_t"] / total_movimentacao_geral) * 100

# Filtros
st.sidebar.header("Filtros")
pais_selecionado = st.sidebar.selectbox("Selecione o País", ["Todos"] + list(resumo["pais"].unique()), index=0)
tipo_produto_selecionado = st.sidebar.selectbox("Selecione o Tipo de Produto", ["Todos"] + list(resumo["tipo_produto"].unique()), index=0)

# Aplicar filtros
if pais_selecionado != "Todos":
    resumo = resumo[resumo["pais"] == pais_selecionado]
if tipo_produto_selecionado != "Todos":
    resumo = resumo[resumo["tipo_produto"] == tipo_produto_selecionado]

# Exibir tabelas
st.subheader("Movimentação por País e Produto")
st.dataframe(resumo, width=1000)

st.subheader("Total por País e Percentual de Exportações")
st.dataframe(resumo_total_pais, width=1000)

# Crédito 
st.write("Fonte: Estatístico Aquaviário ANTAQ")
st.markdown("<p><strong>Ferramenta desenvolvida por Darliane Cunha.</strong></p>", unsafe_allow_html=True)
