import requests
import config

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

# Ejecutar para obtener el token actualizado
refresh_access_token()
