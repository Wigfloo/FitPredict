import requests
import config
import streamlit as st
def get_activities():
    """Obtiene y muestra las 5 actividades más recientes del atleta"""
    url = f"{config.URL_API}/athlete/activities"
    headers = {"Authorization": f"Bearer {config.ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        activities = response.json()
        st.write("✅ Actividades obtenidas:")
        for i, activity in enumerate(activities[:5]):
            st.write(f"{i+1}. {activity['name']} - {activity['distance']} metros")
    else:
        print("❌ Error al obtener actividades:", response.status_code)
        print(response.json())

# Llamar la función cuando se necesite
# get_activities()
