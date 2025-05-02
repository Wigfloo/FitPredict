import requests
import config
import streamlit as st
def get_activities():
    """Obtiene y muestra actividades entre 3K-3.5K y 20-22 minutos"""
    url = f"{config.URL_API}/athlete/activities"
    headers = {"Authorization": f"Bearer {config.ACCESS_TOKEN}"}
    params = {"per_page": 100, "page": 1}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        activities = response.json()

        # Filtrar entrenamientos por distancia y tiempo
        entrenamientos_filtrados = [
            act for act in activities
            if 3000 <= act.get('distance', 0) <= 3500 and
               1200 <= act.get('moving_time', 0) <= 1320
        ]

        if entrenamientos_filtrados:
            st.write("✅ Entrenamientos entre 3K-3.5K y 20-22 min:")
            for i, activity in enumerate(entrenamientos_filtrados):
                nombre = activity.get('name', 'Sin nombre')
                distancia = activity.get('distance', 0)
                tiempo = activity.get('moving_time', 0)
                st.write(f"{i+1}. {nombre} - {distancia} m - {tiempo} seg")
        else:
            st.warning("😕 No se encontraron entrenamientos en ese rango.")
    else:
        print("❌ Error al obtener actividades:", response.status_code)
        print(response.json())
