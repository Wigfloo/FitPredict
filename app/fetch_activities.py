import requests
import config  # Asegúrate de que este archivo contenga URL_API y ACCESS_TOKEN
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# --- Inicialización de Firebase ---
# Reemplaza 'firebase_credentials.json' con la ruta a tu archivo de credenciales
cred = credentials.Certificate("firebase_credentials.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
ACTIVITIES_COLLECTION = "strava_activities"

def upload_activity_to_firebase(activity_data):
    """Sube solo la distancia y el ID de una actividad a Firestore."""
    try:
        activity_id = activity_data.get('id')
        distance = activity_data.get('distance')
        name = activity_data.get('name', 'sin nombre') # Para el mensaje de éxito

        if activity_id is not None and distance is not None:
            data_to_upload = {
                'id': activity_id,
                'distance': distance
            }
            doc_ref = db.collection(ACTIVITIES_COLLECTION).document(str(activity_id))
            doc_ref.set(data_to_upload)
            st.success(f"✅ Actividad '{name}' (ID: {activity_id}) subida a Firebase (solo distancia e ID).")
        else:
            st.warning(f"⚠️ No se pudo obtener ID o distancia para la actividad '{name}'. No se subió a Firebase.")

    except Exception as e:
        st.error(f"❌ Error al subir la actividad '{activity_data.get('name', 'sin nombre')}' (ID: {activity_data.get('id')}) a Firebase: {e}")


def get_activities():
    """
    Obtiene las 5 actividades más recientes del atleta desde la API de Strava
    y muestra en Streamlit solo aquellas cuya distancia está entre 3000 y 3500 metros,
    luego las sube a Firebase.
    """
    url = f"{config.URL_API}/athlete/activities"
    headers = {"Authorization": f"Bearer {config.ACCESS_TOKEN}"}
    params = {'per_page': 5, 'page': 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        activities = response.json()

        if not activities:
            st.info("✅ No se encontraron actividades recientes para mostrar.")
            return

        st.write("✅ Últimas 5 actividades obtenidas. Mostrando y subiendo a Firebase aquellas entre 3000 y 3500 metros:")

        contador_mostradas = 0
        for activity in activities:
            distance = activity.get('distance', 0)

            if 3000 <= distance <= 3500:
                contador_mostradas += 1
                name = activity.get('name', 'Actividad sin nombre')
                st.write(f"{contador_mostradas}. {name} - {distance} metros")
                upload_activity_to_firebase(activity) # Subir la actividad a Firebase

        if contador_mostradas == 0:
            st.info("ℹ️ Ninguna de las últimas 5 actividades tiene una distancia entre 3000 y 3500 metros.")

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ Error HTTP al obtener actividades: {http_err}")
        try:
            error_details = response.json()
            st.json(error_details)
        except Exception:
            st.text(response.text)
    except requests.exceptions.RequestException as req_err:
        st.error(f"❌ Error de conexión o solicitud: {req_err}")
    except Exception as e:
        st.error(f"❌ Ocurrió un error inesperado: {e}")

# --- Cómo llamar la función en tu script principal de Streamlit ---
# import streamlit as st
# from tu_archivo import get_activities

# st.title("Mis Actividades de Strava")
# st.write("Buscando y subiendo actividades recientes...")

# if st.button("Buscar y Subir Actividades Filtradas"):
#      get_activities()

# O simplemente llamarla directamente si quieres que se ejecute al cargar la página:
# get_activities()