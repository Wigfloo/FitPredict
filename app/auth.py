import requests
import config
import streamlit as st

CODE = ''

def refresh_access_token():
    """Renueva el Access Token usando el Refresh Token"""
    url = "https://www.strava.com/oauth/token"
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
        print("✅ Access Token Renovado:", config.ACCESS_TOKEN)
    else:
        print("❌ Error al renovar token:", response.status_code)
        print(response.json())

def getAccessToken():
    uri_exchange = f"{config.URL_API}/oauth/token"
    params = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "code": CODE,
        "grant_type": "authorization_code"
    }
    response = requests.post(uri_exchange, data=params)
    if response.status_code == 200:
        getResponse = response.json()
        refresh_token = getResponse['refresh_token']
        athlete = getResponse['athlete']
        config.REFRESH_TOKEN = refresh_token
        print("✅ Refresh Token:", refresh_token)
        print("✅ Athlete:", athlete)
        #guardar session en el navegador de token y la informacion del usuario del 
        return True
    else:
        print("❌ Error al obtener token:", response.status_code)
        print(response.json())
        print(f'Mi codigo: {CODE}')
        return False


def checkAuthorization():
    #Validar primero que exista una seccion de navegador del usuario donde deben estar guardado el token del usuario y el json con la info del usuario, para no volver a pedir esta informacion
    query_params = st.query_params
    if "code" in query_params:
        global CODE
        CODE = query_params['code']
        return getAccessToken()
    return False