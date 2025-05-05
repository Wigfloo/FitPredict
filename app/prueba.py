import streamlit as st
try:
    with open('perfil.h5', 'rb') as f:
        st.success("¡Archivo encontrado!")
except FileNotFoundError:
    st.error("¡Archivo NO encontrado!")
