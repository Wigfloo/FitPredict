import requests
import config

def get_athlete_data():
    """Obtiene y muestra la información del atleta"""
    url = "https://www.strava.com/api/v3/athlete"
    headers = {"Authorization": f"Bearer {config.ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ Datos del atleta:")
        print(response.json())
    else:
        print("❌ Error al obtener datos:", response.status_code)
        print(response.json())

# Llamar la función solo cuando se necesite
# get_athlete_data()
