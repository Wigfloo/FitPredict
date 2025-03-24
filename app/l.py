import streamlit as st
st.text_input("Nombre", key="loquera")

# You can access the value at any point with:
st.session_state.loquera