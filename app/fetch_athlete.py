import requests
import config
import streamlit as st
def get_athlete_data():
    """Obtiene y muestra la información del atleta"""
    url = "https://www.strava.com/api/v3/athlete"
    headers = {"Authorization": f"Bearer {config.ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        st.write("✅ Datos del atleta:")
        st.write(response.json())
    else:
        st.write("❌ Error al obtener datos:", response.status_code)
        st.write(response.json())

# Llamar la función solo cuando se necesite
# get_athlete_data()
