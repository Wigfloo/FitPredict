import streamlit as st
import config

def getAuthorization():
    REDIRECT_URI = "http://localhost:8501"  # O la URL pública de tu app

    auth_url = f"https://www.strava.com/oauth/authorize?client_id={config.CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=read,activity:read"

    st.markdown(f"[Iniciar sesión con Strava]({auth_url})")
