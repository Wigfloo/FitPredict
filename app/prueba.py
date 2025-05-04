import streamlit as st
try:
    with open('modelo_perfil/perfil.h5', 'rb') as f:
        st.success("¡Archivo encontrado!")
except FileNotFoundError:
    st.error("¡Archivo NO encontrado!")
