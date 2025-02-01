import streamlit as st
import pandas as pd

# Carregar o arquivo
@st.cache_data
def load_data():
    file_path = "data.xlsx"


# Configuração do Streamlit
st.title("Movimentação Portuária por Produto e País")

# Mostrar um preview dos dados
st.write("Pré-visualização dos dados:")
st.dataframe(df.head())

# Filtro por país
pais = st.selectbox("Selecione um país:", df['País'].unique())
df_filtrado = df[df['País'] == pais]
st.write(f"Dados filtrados para {pais}:")
st.dataframe(df_filtrado)

# Gráfico de movimentação por produto
st.write("Movimentação por Produto")
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
df_filtrado.groupby("Produto")["Movimentação"].sum().plot(kind='bar', ax=ax)
ax.set_ylabel("Movimentação (toneladas)")
st.pyplot(fig)
