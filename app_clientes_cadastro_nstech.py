import streamlit as st
import pandas as pd
from cryptography.fernet import Fernet
import os
import io

def login():
    senha = st.text_input("Digite a senha", type="password")

    contrasenha = st.secrets["SENHA_ACESSO"]
    if senha == contrasenha
        st.session_state["logado"] = True
    else:
        st.warning("Senha incorreta")
        st.stop()

if "logado" not in st.session_state:
    login()


# ======================
# 🔐 CARREGAR CHAVE SEGURA
# ======================
key = st.secrets["COFRE_KEY"]

if not key:
    st.error("Chave de criptografia não encontrada!")
    st.stop()

fernet = Fernet(key.encode())

# ======================
# 🔓 DESCRIPTOGRAFAR BASE
# ======================
try:
    with open("base.enc", "rb") as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)

    df = pd.read_excel(io.BytesIO(decrypted))

except Exception:
    st.error("Erro ao descriptografar a base. Verifique a chave.")
    st.stop()

# ======================
# AJUSTES
# ======================
df["CNPJ_CLIENTE"] = df["CNPJ_CLIENTE"].astype(str).str.zfill(14)

st.title("Clientes Cadastro Nstech")

# ======================
# FILTROS (igual ao seu)
# ======================
col1, col2, col3, col4, col5 = st.columns(5)

nomes_originais = df["NOME_CLIENTE"].dropna().unique()
nomes_mapeados = {nome.lower(): nome for nome in nomes_originais}

with col1:
    filtro_cliente_lower = st.multiselect(
        "Nome Cliente",
        options=sorted(nomes_mapeados.keys()),
        format_func=lambda x: nomes_mapeados[x]
    )

with col2:
    filtro_cnpj = st.multiselect("CNPJ", df["CNPJ_CLIENTE"].unique())

with col3:
    filtro_raiz = st.multiselect("Raiz", df["raiz"].astype(str).unique())

with col4:
    filtro_dom = st.multiselect("Domínio", df["Emails"].unique())

with col5:
    filtro_emp = st.multiselect("Tipo intersecção", df["Tipo Intersecção"].astype(str).unique())

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

df_limite = df_filtrado.head(5)

st.data_editor(
    df_limite,
    use_container_width=True,
    height=240,
    disabled=True
)
