import streamlit as st
import auth
import fetch_athlete
import fetch_activities
import acces_code as acc
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
import pickle
import requests
import config
from datetime import datetime, timedelta

# --- Cargar tu modelo, scaler y label encoder entrenados para el PERFIL ---
try:
    # La carpeta modelo_perfil ya no existe, el archivo está en la raíz, con f-string
    ruta_modelo_perfil = f'perfil.h5'

    # model_perfil = load_model(ruta_modelo_perfil)
    load_model = tf.keras.models.load_model(ruta_modelo_perfil)

    ruta_scaler_perfil = f'scaler.pkl'
    with open(ruta_scaler_perfil, 'rb') as file:
        scaler_perfil = pickle.load(file)

    ruta_label_encoder_perfil = f'label_encoder.pkl'
    with open(ruta_label_encoder_perfil, 'rb') as file:
        label_encoder_perfil = pickle.load(file)
except FileNotFoundError as e:
    st.error(
        f"Error al cargar los archivos del modelo de perfil o preprocesamiento: {e}. Asegúrate de que los archivos estén en la misma ubicación que este script."
    )
    st.stop()

# --- Cargar los modelos y scaler entrenados para la PREDICCIÓN DE CARRERA ---
try:
    ruta_modelo_5k = f'modelo_5k.pkl'
    model_carrera_5k = pickle.load(open(ruta_modelo_5k, 'rb'))

    ruta_modelo_10k = f'modelo_10k.pkl'
    model_carrera_10k = pickle.load(open(ruta_modelo_10k, 'rb'))

    ruta_scaler_carrera = f'scaler_3k_pred.pkl'
    scaler_carrera = pickle.load(open(ruta_scaler_carrera, 'rb'))
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
    predicciones = load_model.predict(persona_secuencia_scaled)
    clase_predicha_encoded = np.argmax(predicciones)
    clase_predicha = label_encoder_perfil.inverse_transform(
        [clase_predicha_encoded])[0]

    return clase_predicha, predicciones


def main():
    st.set_page_config(page_title="FitPredict - Strava Sync", page_icon="🏃")

    # Encabezado grande con estilo
    st.markdown(
         "<h1 style='text-align: center; color: #FF4B4B;'>🏃‍♂️ Bienvenido a <span style='color:#1E90FF;'>FitPredict</span></h1>",
          unsafe_allow_html=True
         )

     # Subtítulo centrado
    st.markdown(
          "<p style='text-align: center; font-size:18px;'>Conectá tu cuenta de Strava para empezar a analizar tu rendimiento como un pro.</p>",
          unsafe_allow_html=True
          )

      # Línea divisoria visual
    st.markdown("<hr style='border:1px solid #ddd;'>",
                   unsafe_allow_html=True)

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

                            # --- INICIO DEL CÓDIGO COMBINADO (CODIGO 1) ---
                            if predicted_profile:
                                st.subheader(f"Perfil predicho basado en las últimas actividades: {predicted_profile.upper()}")
                                perfil_normalizado = predicted_profile.lower().strip()

                                if perfil_normalizado == "elite":
                                    st.success("💪 ¡Impresionante! Tu rendimiento te coloca en la categoría de atleta de élite. ¡Sigue así!")

                                    entrenamiento_elite = {
                                        "Semana": [f"{i+1}" for i in range(8)],
                                        "Día 1": ["Correr 10 km", "Fartlek: 5 min rápido x4", "Correr 15 km", "Intervalos: 10x1000m", "Correr 15 km", "Correr 9 km", "Fartlek: 8 min rápido x5", "Correr 15 km"],
                                        "Día 2": ["Correr 10 km", "Descanso", "Correr 15 km", "Intervalos: 10x1000m", "Correr 15 km", "Descanso", "Fartlek: 8 min rápido x5", "Descanso"],
                                        "Día 3": ["Descanso", "Fartlek: 5 min rápido x4", "Correr 15 km", "Fartlek: 8 min rápido x3", "Descanso", "Correr 9 km", "Descanso", "Correr 15 km"],
                                        "Día 4": ["Correr 15 km", "Intervalos: 10x800m", "Descanso", "Descanso", "Correr 15 km", "Descanso", "Correr 15 km", "Descanso"],
                                        "Día 5": ["Correr 15 km", "Intervalos: 10x800m", "Correr 18 km", "Fartlek: 8 min rápido x3", "Descanso", "Intervalos: 6x800m", "Descanso", "Correr 18 km"],
                                        "Día 6": ["Descanso", "Intervalos: 10x800m", "Descanso", "Descanso", "Correr 18 km", "Descanso", "Correr 18 km", "Correr 20 km"],
                                        "Día 7": ["Correr 7 km", "Descanso", "Correr 8 km", "Fartlek: 5 min rápido x3", "Descanso", "Intervalos: 6x800m", "Descanso", "Descanso"]
                                    }
                                    st.markdown("### 📋 Plan de entrenamiento (Élite)")
                                    st.dataframe(entrenamiento_elite)

                                elif perfil_normalizado == "intermedio":
                                    st.info("⚡ ¡Muy bien! Estás en un nivel intermedio, mostrando un progreso constante. ¡Mantén el esfuerzo!")

                                    entrenamiento_intermedio = {
                                        "Semana": [f"{i+1}" for i in range(8)],
                                        "Día 1": ["Correr 4 km", "Correr 5 km", "Correr 5 km", "Fartlek: 1 min rápido x4", "Correr 6 km", "Correr 7 km", "Fartlek: 2 min rápido x4", "Correr 8 km"],
                                        "Día 2": ["Descanso", "Correr 5 km", "Descanso", "Fartlek: 1 min rápido x4", "Descanso", "Descanso", "Fartlek: 2 min rápido x4", "Descanso"],
                                        "Día 3": ["Correr 4 km", "Descanso", "Correr 5 km", "Descanso", "Correr 6 km", "Correr 7 km", "Descanso", "Correr 8 km"],
                                        "Día 4": ["Descanso", "Correr 5 km", "Descanso", "Fartlek: 2 min rápido x4", "Descanso", "Descanso", "Correr 7 km", "Descanso"],
                                        "Día 5": ["Correr 4 km", "Intervalos: 3x800m", "Correr 6 km", "Descanso", "Correr 6 km", "Intervalos: 4x800m", "Descanso", "Correr 10 km"],
                                        "Día 6": ["Descanso", "Intervalos: 3x800m", "Descanso", "Fartlek: 2 min rápido x4", "Descanso", "Descanso", "Correr 7 km", "Descanso"],
                                        "Día 7": ["Correr 5 km", "Descanso", "Correr 6 km", "Descanso", "Correr 6 km", "Intervalos: 4x800m", "Descanso", "Correr 10 km"]
                                    }
                                    st.markdown("### 📋 Plan de entrenamiento (Intermedio)")
                                    st.dataframe(entrenamiento_intermedio)

                                elif perfil_normalizado == "novato":
                                    st.warning("🚀 ¡Excelente comienzo! Estás en la etapa de novato, cada entrenamiento cuenta. ¡No te rindas!")

                                    entrenamiento_novato = {
                                        "Semana": [f"{i+1}" for i in range(8)],
                                        "Día 1": ["Caminar 20 min", "Caminar 5 min + trotar 1 min (x4)", "Trotar 1 min / caminar 1 min (x6)", "Trotar 2 min / caminar 1 min (x6)", "Trotar 3 min / caminar 1 min (x5)", "Trotar 5 min / caminar 1 min (x4)", "Trotar 7 min / caminar 1 min (x3)", "Correr 5 km suave"],
                                        "Día 2": ["Descanso", "Caminar 30 min", "Trotar 1 min / caminar 1 min (x6)", "Trotar 2 min / caminar 1 min (x6)", "Descanso", "Trotar 5 min / caminar 1 min (x4)", "Descanso", "Descanso"],
                                        "Día 3": ["Caminar 20 min", "Caminar 5 min + trotar 1 min (x4)", "Trotar 1 min / caminar 1 min (x6)", "Descanso", "Trotar 3 min / caminar 1 min (x5)", "Descanso", "Trotar 7 min / caminar 1 min (x3)", "Correr 5 km suave"],
                                        "Día 4": ["Descanso", "Descanso", "Descanso", "Trotar 2 min / caminar 1 min (x6)", "Descanso", "Trotar 5 min / caminar 1 min (x4)", "Descanso", "Descanso"],
                                        "Día 5": ["Caminar 25 min", "Caminar 5 min + trotar 1 min (x4)", "Trotar 1 min / caminar 1 min (x6)", "Descanso", "Trotar 3 min / caminar 1 min (x5)", "Descanso", "Trotar 7 min / caminar 1 min (x3)", "Correr 5 km suave"],
                                        "Día 6": ["Descanso", "Caminar 30 min", "Trotar 1 min / caminar 1 min (x6)", "Trotar 2 min / caminar 1 min (x6)", "Descanso", "Descanso", "Descanso", "Descanso"],
                                        "Día 7": ["Caminar 25 min", "Descanso", "Descanso", "", "Trotar 3 min / caminar 1 min (x5)", "", "Trotar 7 min / caminar 1 min (x3)", "Correr 5 km suave"]
                                    }
                                    st.markdown("### 📋 Plan de entrenamiento (Novato)")
                                    st.dataframe(entrenamiento_novato)

                                else:
                                    st.info("🔍 No se pudo determinar un perfil válido para mostrar un plan de entrenamiento.")
                            else:
                                st.warning("❌ No se pudo realizar la predicción con los datos obtenidos.")
                            # --- FIN DEL CÓDIGO COMBINADO (CODIGO 1) ---

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

                            st.subheader(
                                "Predicciones de Rendimiento en Carrera:")
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
            st.warning(
                "🔒 Necesitás conectar tu cuenta de Strava para continuar.")
            acc.getAuthorization()


if __name__ == "__main__":
    main()
