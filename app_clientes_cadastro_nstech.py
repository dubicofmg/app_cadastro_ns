import streamlit as st
import pandas as pd

df = pd.read_excel("Fonte_bi_clientes_cadastro.xlsx")

st.title("Clientes Cadastro Nstech")

# Cria filtros para cada coluna desejada
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    filtro_cliente = st.multiselect("Nome Cliente", df["NOME_CLIENTE"].unique())

with col2:
    filtro_cnpj = st.multiselect("CNPJ", df["CNPJ_CLIENTE"].unique())

with col3:
    filtro_raiz = st.multiselect("Raiz", df["raiz"].astype(str).unique())

with col4:
    filtro_dom = st.multiselect("Domínio", df["Emails"].unique())

with col5:
    filtro_emp = st.multiselect("Tipo intersecção", df["Tipo Intersecção"].astype(str).unique())

# Aplicando os filtros
df_filtrado = df.copy()

if filtro_cliente:
    df_filtrado = df_filtrado[df_filtrado["NOME_CLIENTE"].isin(filtro_cliente)]
if filtro_cnpj:
    df_filtrado = df_filtrado[df_filtrado["CNPJ_CLIENTE"].isin(filtro_cnpj)]
if filtro_raiz:
    df_filtrado = df_filtrado[df_filtrado["raiz"].astype(str).isin(filtro_raiz)]
if filtro_dom:
    df_filtrado = df_filtrado[df_filtrado["Emails"].isin(filtro_dom)]
if filtro_emp:
    df_filtrado = df_filtrado[df_filtrado["Tipo Intersecção"].astype(str).isin(filtro_emp)]

# Limita visualização a 5 linhas
df_limite = df_filtrado.head(5)

# Exibe a tabela em modo leitura, permitindo copiar
st.data_editor(
    df_limite,
    use_container_width=True,
    height=240,  # ajuste de altura para 5 linhas
    disabled=True  # impede edição, mas permite cópia
)
