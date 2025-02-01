import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para formatar números no padrão brasileiro
def formatar_numeros(df, colunas):
    for coluna in colunas:
        df[coluna] = df[coluna].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if pd.notnull(x) else x)
    return df

# Carregar o arquivo
@st.cache_data
def load_data():
    file_path = "data.xlsx"
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        
        # Padronizar nomes das colunas
        colunas_originais = df.columns.tolist()
        colunas_novas = [c.strip().lower() for c in colunas_originais]  # Remove espaços e coloca em minúsculas
        mapeamento = {
            "país": "País",
            "produto": "Produto",
            "movimentação": "Movimentação",
            "ano": "Ano"
        }
        
        df.columns = [mapeamento.get(c, c) for c in colunas_novas]  # Renomeia colunas se necessário
        
        # Verificar se todas as colunas necessárias existem
        required_columns = {"País", "Produto", "Movimentação", "Ano"}
        if not required_columns.issubset(df.columns):
            st.error(f"O arquivo não contém todas as colunas esperadas: {required_columns}. Colunas encontradas: {df.columns.tolist()}")
            return None

        # Ajustar números para padrão brasileiro
        df = formatar_numeros(df, ["Movimentação"])

        # Converter anos para formato correto (YYYY)
        df["Ano"] = df["Ano"].astype(str).str.extract(r'(\d{4})')  # Garante que os anos tenham 4 dígitos

        return df
    except FileNotFoundError:
        st.error("Erro: O arquivo 'data.xlsx' não foi encontrado. Verifique se ele está no diretório correto.")
        return None
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
    
    # Filtro por país
    pais = st.selectbox("Selecione um país:", df['País'].unique())
    df_filtrado = df[df['País'] == pais]

    # Filtro por ano
    anos = sorted(df_filtrado['Ano'].unique())
    ano_selecionado = st.selectbox("Selecione um ano:", anos)
    df_filtrado = df_filtrado[df_filtrado['Ano'] == ano_selecionado]

    st.write(f"Dados filtrados para {pais} no ano {ano_selecionado}:")
    st.dataframe(df_filtrado)

    # Gráfico de movimentação por produto
    st.write("Movimentação por Produto")
    fig, ax = plt.subplots()
    df_filtrado.groupby("Produto")["Movimentação"].sum().plot(kind='bar', ax=ax)
    ax.set_ylabel("Movimentação (toneladas)")
    st.pyplot(fig)
else:
    st.warning("Nenhum dado foi carregado. Verifique o arquivo e tente novamente.")
