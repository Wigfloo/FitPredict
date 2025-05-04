import streamlit as st
import auth
import fetch_athlete
import fetch_activities
import acces_code as acc
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import load_model
import pickle

# --- Cargar tu modelo, scaler y label encoder entrenados ---
try:
    model = load_model('tu_modelo_lstm.h5')
    with open('scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
    with open('label_encoder.pkl', 'rb') as file:
        label_encoder = pickle.load(file)
except FileNotFoundError as e:
    st.error(f"Error al cargar los archivos del modelo o preprocesamiento: {e}. Asegúrate de que los archivos estén en la misma ubicación que este script.")
    st.stop()

N_STEPS = 1060 # Debe coincidir con la longitud de secuencia de tu modelo
FEATURES = ['Frecuencia_cardiaca_prom', 'Ritmo_min_km', 'Distancia_metros']

def predecir_perfil_con_ultimos_datos(strava_data):
    """
    Toma una lista de diccionarios (datos de las últimas actividades de Strava),
    preprocesa los datos y predice el perfil utilizando el modelo LSTM.
    """
    if not strava_data:
        st.warning("No se proporcionaron datos de Strava para la predicción.")
        return None, None

    data_for_model = []
    for activity in strava_data:
        if all(key in activity for key in ['average_heartrate', 'average_speed', 'distance', 'start_date_local']):
            heart_rate = activity['average_heartrate']
            speed_mps = activity['average_speed']
            distance_meters = activity['distance']
            date_activity = activity['start_date_local']

            # Calcular el ritmo en minutos por kilómetro
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

    if not data_for_model:
        st.warning("No se encontraron datos válidos (ritmo, FC, distancia) en los datos de Strava.")
        return None, None

    persona_df = pd.DataFrame(data_for_model).sort_values(by='Fecha_actividad')

    # Tomar las últimas N_STEPS actividades (o todas si son menos)
    persona_secuencia = persona_df[FEATURES].tail(N_STEPS).values

    if len(persona_secuencia) < N_STEPS:
        padding_length = N_STEPS - len(persona_secuencia)
        padding = np.zeros((padding_length, len(FEATURES)))
        persona_secuencia = np.concatenate((padding, persona_secuencia))

    # Escalar la secuencia
    persona_secuencia_scaled = scaler.transform(persona_secuencia)
    persona_secuencia_scaled = persona_secuencia_scaled.reshape(1, N_STEPS, len(FEATURES))

    # Realizar la predicción
    predicciones = model.predict(persona_secuencia_scaled)
    clase_predicha_encoded = np.argmax(predicciones)
    clase_predicha = label_encoder.inverse_transform([clase_predicha_encoded])[0]

    return clase_predicha, predicciones

def main():
    st.set_page_config(page_title="FitPredict - Strava Sync", page_icon="🏃")
    st.title("🏃 Bienvenido a FitPredict")
    st.write("Conectá tu cuenta de Strava para empezar a analizar tu rendimiento.")

    if auth.checkAuthorization():
        st.success("✅ Conexión con Strava exitosa!")

        opcion = st.selectbox("¿Qué deseas hacer?", ["Selecciona una opción", "Ver mi perfil", "Ver datos de actividad para el modelo y predecir"])

        if opcion == "Ver mi perfil":
            fetch_athlete.get_athlete_data()

        elif opcion == "Ver datos de actividad para el modelo y predecir":
            if st.button("Obtener datos y predecir"):
                with st.spinner("Obteniendo datos recientes de Strava..."):
                    latest_activities = fetch_activities.get_activities_raw() # Usar el valor predeterminado de per_page en fetch_activities
                if latest_activities:
                    with st.spinner("Preprocesando datos y prediciendo..."):
                        predicted_profile, probabilities = predecir_perfil_con_ultimos_datos(latest_activities)
                    if predicted_profile:
                       st.subheader(f"Perfil predicho basado en las últimas actividades: **{predicted_profile.upper()}!**") # Mostramos la clase predicha en mayúsculas
                       st.write("Probabilidades:")
                       st.write(probabilities)
                    else:
                        st.warning("No se pudo realizar la predicción con los datos obtenidos.")
                else:
                    st.warning("No se encontraron actividades recientes para realizar la predicción.")

    else:
        st.warning("🔒 Necesitás conectar tu cuenta de Strava para continuar.")
        acc.getAuthorization()

if __name__ == "__main__":
    main()