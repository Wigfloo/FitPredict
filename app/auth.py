import requests
import config
import streamlit as st

# Variables globales temporales (podrían migrarse a sesión en el futuro)
CODE = ''


def refresh_access_token():
    """Renueva el Access Token usando el Refresh Token almacenado"""
    url = f"{config.URL_API}/oauth/token"
    params = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": config.REFRESH_TOKEN
    }

    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        new_tokens = response.json()
        config.ACCESS_TOKEN = new_tokens["access_token"]
        config.REFRESH_TOKEN = new_tokens["refresh_token"]
        print("✅ Access Token Renovado:", config.ACCESS_TOKEN)
    else:
        print("❌ Error al renovar token:", response.status_code)
        print(response.json())


def getAccessToken():
    """Intercambia el 'code' por un Access Token"""
    uri_exchange = f"{config.URL_API}/oauth/token"
    params = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "code": CODE,
        "grant_type": "authorization_code"
    }

    response = requests.post(uri_exchange, data=params)

    if response.status_code == 200:
        data = response.json()
        config.ACCESS_TOKEN = data['access_token']
        config.REFRESH_TOKEN = data['refresh_token']
        st.session_state['token_obtenido'] = True
        print("✅ Access Token generado")
        return True
    else:
        print("❌ Error al obtener token:", response.status_code)
        print(response.json())
        print(f"Mi codigo: {CODE}")
        return False


def checkAuthorization():
    """
    Verifica si ya se autorizó el acceso a la API de Strava.
    Si hay un código en la URL y no se ha procesado, lo intercambia por un token.
    """
    query_params = st.query_params

    if "code" in query_params and not st.session_state.get('token_obtenido', False):
        global CODE
        code_param = query_params.get("code", None)
        if isinstance(code_param, list):
            CODE = code_param[0]
        else:
            CODE = code_param
        return getAccessToken()

    elif st.session_state.get('token_obtenido', False):
        return True

    return False