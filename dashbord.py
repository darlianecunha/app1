import streamlit as st
import pandas as pd
import subprocess
import sys

# Garantir que matplotlib esteja instalado
def install_and_import(package):
    try:
        __import__(package)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        __import__(package)

install_and_import("matplotlib")
import matplotlib.pyplot as plt

# Carregar o arquivo
@st.cache_data
def load_data():
    file_path = "data.xlsx"
    try:
        df = pd.read_excel(file_path, engine="data")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

df = load_data()

# Configuração do Streamlit
st.title("Movimentação Portuária por Produto e País")

if df is not None:
    # Mostrar um preview dos dados
    st.write("Pré-visualização dos dados:")
    st.dataframe(df.head())
    
    # Verificar se as colunas necessárias existem
    required_columns = {"País", "Produto", "Movimentação"}
    if required_columns.issubset(df.columns):
        # Filtro por país
        pais = st.selectbox("Selecione um país:", df['País'].unique())
        df_filtrado = df[df['País'] == pais]
        st.write(f"Dados filtrados para {pais}:")
        st.dataframe(df_filtrado)
        
        # Gráfico de movimentação por produto
        st.write("Movimentação por Produto")
        fig, ax = plt.subplots()
        df_filtrado.groupby("Produto")["Movimentação"].sum().plot(kind='bar', ax=ax)
        ax.set_ylabel("Movimentação (toneladas)")
        st.pyplot(fig)
    else:
        st.error("O arquivo não contém as colunas esperadas: 'País', 'Produto' e 'Movimentação'.")
else:
    st.warning("Nenhum dado foi carregado. Verifique o arquivo e tente novamente.")
