import requests
import config
import streamlit as st
import pandas as pd
import numpy as np

def get_activities_raw(per_page=30):
    """
    Obtiene las 'per_page' actividades más recientes del atleta desde la API de Strava
    y devuelve la lista de diccionarios JSON sin procesar.
    """
    url = f"{config.URL_API}/athlete/activities"
    headers = {"Authorization": f"Bearer {config.ACCESS_TOKEN}"}
    params = {'per_page': per_page, 'page': 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        activities = response.json()
        return activities
    except requests.exceptions.HTTPError as http_err:
        st.error(f"Error HTTP al obtener actividades: {http_err}")
        try:
            error_details = response.json()
            st.json(error_details)
        except Exception:
            st.text(response.text)
        return None
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error de conexión o solicitud: {req_err}")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
        return None

def get_activities_for_visualization(per_page=10):
    """
    Obtiene las 'per_page' actividades más recientes del atleta desde la API de Strava
    y muestra la fecha, frecuencia cardíaca promedio, ritmo y distancia.
    """
    activities = get_activities_raw(per_page=per_page)
    if not activities:
        st.info("No se encontraron actividades recientes para mostrar.")
        return

    st.subheader(f"Últimas {per_page} Actividades (Datos para el Modelo):")
    for i, activity in enumerate(activities):
        fecha = activity.get('start_date_local', 'Sin fecha').split('T')[0]
        heart_rate = activity.get('average_heartrate', 'N/A')
        speed_mps = activity.get('average_speed')
        distance_meters = activity.get('distance', 'N/A')
        ritmo_min_km = 'N/A'

        if speed_mps and speed_mps > 0:
            ritmo_s_m = 1 / speed_mps
            ritmo_min_km = (ritmo_s_m * 1000) / 60
            ritmo_min_km = f"{int(ritmo_min_km // 1)}:{int(ritmo_min_km % 1 * 60):02d}"

        st.write(f"**Actividad {i+1}:** {fecha}")
        st.write(f"- Frecuencia Cardíaca Promedio: {heart_rate}")
        st.write(f"- Ritmo Promedio (min/km): {ritmo_min_km}")
        st.write(f"- Distancia (metros): {distance_meters}")
        st.write("---")

def get_data_for_model(per_page=100):
    """
    Obtiene las primeras 'per_page' actividades más recientes del atleta desde la API de Strava,
    extrae las características necesarias para el modelo y las devuelve en un DataFrame.
    """
    activities = get_activities_raw(per_page=per_page)
    if not activities:
        return pd.DataFrame()

    data_for_model = []
    for activity in activities:
        if all(key in activity for key in ['average_heartrate', 'average_speed', 'distance', 'start_date_local']):
            heart_rate = activity['average_heartrate']
            speed_mps = activity['average_speed']
            distance_meters = activity['distance']
            date_activity = activity['start_date_local']

            if speed_mps > 0:
                ritmo_s_m = 1 / speed_mps
                ritmo_min_km = (ritmo_s_m * 1000) / 60
            else:
                ritmo_min_km = np.nan

            data_for_model.append({
                'Fecha_actividad': date_activity,
                'Frecuencia_cardiaca_prom': heart_rate,
                'Ritmo_min_km': ritmo_min_km,
                'Distancia_metros': distance_meters
            })
    return pd.DataFrame(data_for_model)

def buscar_prueba_3k_strava():
    """
    Busca en las actividades recientes de Strava una posible prueba de 3000 metros
    y devuelve un diccionario con los datos relevantes o None si no se encuentra.
    """
    activities = get_activities_raw(per_page=100) # Obtener más actividades para buscar
    if not activities:
        return None

    posible_prueba = None
    min_diferencia_distancia = float('inf')
    datos_prueba = {}

    for activity in activities:
        if activity.get('type') == 'Run':
            distancia_km = activity.get('distance', 0) / 1000.0
            # Buscar actividades con una distancia cercana a 3k (ej. +/- 100 metros)
            if 2.9 <= distancia_km <= 3.1:
                diferencia = abs(distancia_km - 3.0)
                if diferencia < min_diferencia_distancia:
                    min_diferencia_distancia = diferencia
                    posible_prueba = activity

    if posible_prueba:
        tiempo_segundos = posible_prueba.get('elapsed_time', 0)
        distancia_metros = posible_prueba.get('distance', 0)
        ritmo_s_m = 1 / posible_prueba.get('average_speed', 0.001) if posible_prueba.get('average_speed', 0) > 0 else np.nan
        ritmo_min_km = (ritmo_s_m * 1000) / 60 if not np.isnan(ritmo_s_m) else np.nan
        frecuencia_cardiaca_prom = posible_prueba.get('average_heartrate')
        frecuencia_cardiaca_max = posible_prueba.get('max_heartrate')

        datos_prueba = {
            'Tiempo_segundos': tiempo_segundos,
            'Ritmo_min_km': ritmo_min_km,
            'Frecuencia_cardiaca_prom_3k': frecuencia_cardiaca_prom,
            'Frecuencia_cardiaca_max_3k': frecuencia_cardiaca_max
        }
        return datos_prueba
    else:
        st.info("No se encontró automáticamente una prueba de 3000 metros reciente en tus actividades de Strava.")
        return None
