import streamlit as st
import pandas as pd

# Carrega o DataFrame
df = pd.read_excel("Fonte_bi_clientes_cadastro.xlsx")

# Ajusta o campo CNPJ para string com 14 dígitos (com zeros à esquerda)
df["CNPJ_CLIENTE"] = df["CNPJ_CLIENTE"].astype(str).str.zfill(14)

st.title("Clientes Cadastro Nstech")

# Cria filtros para cada coluna desejada
col1, col2, col3, col4, col5 = st.columns(5)

# ======== Filtro Nome Cliente (com busca case-insensitive) ========
nomes_originais = df["NOME_CLIENTE"].dropna().unique()
nomes_mapeados = {nome.lower(): nome for nome in nomes_originais}

with col1:
    filtro_cliente_lower = st.multiselect(
        "Nome Cliente",
        options=sorted(nomes_mapeados.keys()),
        format_func=lambda x: nomes_mapeados[x]
    )

# ======== Filtro CNPJ (com zeros à esquerda) ========
with col2:
    filtro_cnpj = st.multiselect("CNPJ", df["CNPJ_CLIENTE"].unique())

# ======== Filtro Raiz ========
with col3:
    filtro_raiz = st.multiselect("Raiz", df["raiz"].astype(str).unique())

# ======== Filtro Domínio ========
with col4:
    filtro_dom = st.multiselect("Domínio", df["Emails"].unique())

# ======== Filtro Tipo Intersecção ========
with col5:
    filtro_emp = st.multiselect("Tipo intersecção", df["Tipo Intersecção"].astype(str).unique())

# Aplicando os filtros
df_filtrado = df.copy()

if filtro_cliente_lower:
    nomes_escolhidos = [nomes_mapeados[n] for n in filtro_cliente_lower]
    df_filtrado = df_filtrado[df_filtrado["NOME_CLIENTE"].isin(nomes_escolhidos)]

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
