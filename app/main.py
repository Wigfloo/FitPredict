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
import requests
import config
from datetime import datetime, timedelta

# --- Cargar tu modelo, scaler y label encoder entrenados para el PERFIL ---
try:
    model_perfil = load_model("perfil.h5")
    with open("scaler.pkl", 'rb') as file:
        scaler_perfil = pickle.load(file)
    with open("label_encoder.pkl", 'rb') as file:
        label_encoder_perfil = pickle.load(file)
except FileNotFoundError as e:
    st.error(
        f"Error al cargar los archivos del modelo de perfil o preprocesamiento: {e}. Asegúrate de que los archivos estén en la misma ubicación que este script."
    )
    st.stop()

# --- Cargar los modelos y scaler entrenados para la PREDICCIÓN DE CARRERA ---
try:
    model_carrera_5k = pickle.load(open("modelo_5k.pkl", 'rb'))
    model_carrera_10k = pickle.load(
        open("modelo_10k.pkl", 'rb'))
    scaler_carrera = pickle.load(
        open("scaler_3k_pred.pkl", 'rb'))
except FileNotFoundError as e:
    st.error(f"Error al cargar los archivos del modelo de carrera: {e}")
    st.stop()

N_STEPS = 1060  # Debe coincidir con la longitud de secuencia de tu modelo de PERFIL
FEATURES = ['Frecuencia_cardiaca_prom', 'Ritmo_min_km', 'Distancia_metros']


def buscar_prueba_3k_strava():
    """
    Busca en las actividades recientes de Strava una posible prueba de 3000 metros
    y devuelve un diccionario con los datos relevantes o None si no se encuentra.
    """
    activities = fetch_activities.get_activities_raw(
        per_page=100)  # Usar la función existente
    if not activities:
        return None

    posible_prueba = None
    min_diferencia_distancia = float('inf')
    datos_prueba = {}

    for activity in activities:
        if activity.get('type') == 'Run':
            distancia_km = activity.get('distance', 0) / 1000.0
            if 2.9 <= distancia_km <= 3.1:
                diferencia = abs(distancia_km - 3.0)
                if diferencia < min_diferencia_distancia:
                    min_diferencia_distancia = diferencia
                    posible_prueba = activity

    if posible_prueba:
        tiempo_segundos = posible_prueba.get('elapsed_time', 0)
        distancia_metros = posible_prueba.get('distance', 0)
        ritmo_s_m = 1 / posible_prueba.get('average_speed', 0.001) if posible_prueba.get(
            'average_speed', 0) > 0 else np.nan
        ritmo_min_km = (ritmo_s_m * 1000) / \
            60 if not np.isnan(ritmo_s_m) else np.nan
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
        st.info(
            "No se encontró automáticamente una prueba de 3000 metros reciente en tus actividades de Strava.")
        return None


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
        if all(
            key in activity
            for key in ['average_heartrate', 'average_speed', 'distance', 'start_date_local']
        ):
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

            data_for_model.append(
                {
                    'Fecha_actividad': date_activity,
                    'Frecuencia_cardiaca_prom': heart_rate,
                    'Ritmo_min_km': ritmo_min_km,
                    'Distancia_metros': distance_meters,
                }
            )

    if not data_for_model:
        st.warning(
            "No se encontraron datos válidos (ritmo, FC, distancia) en los datos de Strava.")
        return None, None

    persona_df = pd.DataFrame(data_for_model).sort_values(by='Fecha_actividad')

    # Tomar las últimas N_STEPS actividades (o todas si son menos)
    persona_secuencia = persona_df[FEATURES].tail(N_STEPS).values

    if len(persona_secuencia) < N_STEPS:
        padding_length = N_STEPS - len(persona_secuencia)
        padding = np.zeros((padding_length, len(FEATURES)))
        persona_secuencia = np.concatenate((padding, persona_secuencia))

    # Escalar la secuencia
    persona_secuencia_scaled = scaler_perfil.transform(persona_secuencia)
    persona_secuencia_scaled = persona_secuencia_scaled.reshape(
        1, N_STEPS, len(FEATURES))

    # Realizar la predicción
    predicciones = model_perfil.predict(persona_secuencia_scaled)
    clase_predicha_encoded = np.argmax(predicciones)
    clase_predicha = label_encoder_perfil.inverse_transform(
        [clase_predicha_encoded])[0]

    return clase_predicha, predicciones


def main():
    st.set_page_config(page_title="FitPredict - Strava Sync", page_icon="🏃")
    st.title("🏃 Bienvenido a FitPredict")
    st.write("Conectá tu cuenta de Strava para empezar a analizar tu rendimiento.")

    if auth.checkAuthorization():
        st.success("✅ Conexión con Strava exitosa!")

        opcion = st.selectbox(
            "¿Qué deseas hacer?",
            [
                "Selecciona una opción",
                "Ver mi perfil",
                "Ver datos de actividad para el modelo y predecir perfil",
                "Predecir mi rendimiento en carrera (basado en prueba de 3k de Strava)"
            ],
        )

        if opcion == "Ver mi perfil":
            fetch_athlete.get_athlete_data()

        elif opcion == "Ver datos de actividad para el modelo y predecir perfil":
            if st.button("Obtener datos y predecir"):
                with st.spinner("Obteniendo datos recientes de Strava..."):
                    latest_activities = fetch_activities.get_activities_raw()
                if latest_activities:
                    with st.spinner("Preprocesando datos y prediciendo..."):
                        predicted_profile, probabilities = predecir_perfil_con_ultimos_datos(
                            latest_activities
                        )

                        if predicted_profile:
                            st.subheader(
                                f"Perfil predicho basado en las últimas actividades: {predicted_profile.upper()}"
                            )
                            perfil_normalizado = predicted_profile.lower().strip()

                            if perfil_normalizado == "elite":
                                st.success(
                                    "¡Impresionante! Tu rendimiento te coloca en la categoría de atleta de élite. ¡Sigue así!")
                            elif perfil_normalizado == "intermedio":
                                st.info(
                                    "¡Muy bien! Estás en un nivel intermedio, mostrando un progreso constante. ¡Mantén el esfuerzo!")
                            elif perfil_normalizado == "novato":
                                st.warning(
                                    "¡Excelente comienzo! Estás en la etapa de novato, cada entrenamiento cuenta. ¡No te rindas!")
                            else:
                                st.write(
                                    "No se pudo determinar un mensaje personalizado para este perfil.")
                        else:
                            st.warning(
                                "No se pudo realizar la predicción con los datos obtenidos.")
                else:
                    st.warning(
                        "No se encontraron actividades recientes para realizar la predicción.")

        elif opcion == "Predecir mi rendimiento en carrera (basado en prueba de 3k de Strava)":
            st.subheader(
                "Predicción de Rendimiento en Carrera usando datos de Strava (Prueba de 3k)")
            prueba_3k_data = buscar_prueba_3k_strava()

            if prueba_3k_data:
                st.subheader("Datos Encontrados de Posible Prueba de 3k:")
                st.write(
                    f"Tiempo: {pd.Timedelta(seconds=int(prueba_3k_data['Tiempo_segundos']))}")
                st.write(
                    f"Ritmo Promedio: {prueba_3k_data['Ritmo_min_km']:.2f} min/km")
                st.write(
                    f"Frecuencia Cardíaca Promedio: {prueba_3k_data.get('Frecuencia_cardiaca_prom_3k', 'N/A')} bpm")
                st.write(
                    f"Frecuencia Cardíaca Máxima: {prueba_3k_data.get('Frecuencia_cardiaca_max_3k', 'N/A')} bpm")

                st.subheader("Ingresa tus datos personales:")
                sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
                edad = st.number_input(
                    "Edad", min_value=10, max_value=100, step=1)
                peso_kg = st.number_input(
                    "Peso (kg)", min_value=30.0, max_value=200.0, step=0.1)
                altura_m = st.number_input(
                    "Altura (m)", min_value=1.0, max_value=2.5, step=0.01)

                if st.button("Predecir mi tiempo en carrera"):
                    if prueba_3k_data['Ritmo_min_km'] is not np.nan and prueba_3k_data['Frecuencia_cardiaca_prom_3k'] is not None and prueba_3k_data['Frecuencia_cardiaca_max_3k'] is not None:
                        sexo_encoded = 1 if sexo == "Masculino" else 0
                        imc = peso_kg / (altura_m ** 2)

                        input_data_carrera = pd.DataFrame({
                            'Ritmo_3k_min_km': [prueba_3k_data['Ritmo_min_km']],
                            'Frecuencia_cardiaca_prom_3k': [prueba_3k_data['Frecuencia_cardiaca_prom_3k']],
                            'Frecuencia_cardiaca_max_3k': [prueba_3k_data['Frecuencia_cardiaca_max_3k']],
                            'Sexo_encoded': [sexo_encoded],
                            'Edad': [edad],
                            'IMC': [imc]
                        })

                        input_scaled_carrera = scaler_carrera.transform(
                            input_data_carrera)

                        prediction_5k = model_carrera_5k.predict(
                            input_scaled_carrera)
                        prediction_10k = model_carrera_10k.predict(
                            input_scaled_carrera)

                        st.subheader("Predicciones de Rendimiento en Carrera:")
                        st.write("**Predicción 5k:**")
                        st.write(
                            f"- Ritmo Promedio Estimado: {prediction_5k[0][0]:.2f} min/km")
                        st.write(
                            f"- Tiempo Estimado: {pd.Timedelta(seconds=int(prediction_5k[0][1]))}")
                        st.write(
                            f"- Frecuencia Cardíaca Promedio Estimada: {prediction_5k[0][2]:.2f} bpm")

                        st.write("**Predicción 10k:**")
                        st.write(
                            f"- Ritmo Promedio Estimado: {prediction_10k[0][0]:.2f} min/km")
                        st.write(
                            f"- Tiempo Estimado: {pd.Timedelta(seconds=int(prediction_10k[0][1]))}")
                        st.write(
                            f"- Frecuencia Cardíaca Promedio Estimada: {prediction_10k[0][2]:.2f} bpm")

                    else:
                        st.warning(
                            "No se encontraron datos suficientes de la prueba de 3k para realizar la predicción de carrera.")

            else:
                st.info(
                    "No se encontraron pruebas de 3000 metros recientes en tus actividades de Strava.")

    else:
        st.warning("🔒 Necesitás conectar tu cuenta de Strava para continuar.")
        acc.getAuthorization()


if __name__ == "__main__":
    main()
