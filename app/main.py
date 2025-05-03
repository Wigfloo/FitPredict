import streamlit as st
import auth
import fetch_athlete
import fetch_activities
import acces_code as acc


def main():
    st.set_page_config(page_title="FitPredict - Strava Sync", page_icon="🏃")
    st.title("🏃 Bienvenido a FitPredict")
    st.write("Conectá tu cuenta de Strava para empezar a analizar tu rendimiento.")

    # 1. Verificamos si ya existe un código de autorización en la URL (usuario ya autorizó)
    if auth.checkAuthorization():
        st.success("✅ Conexión con Strava exitosa!")

        # 2. Mostramos el menú de opciones
        opcion = st.selectbox("¿Qué deseas hacer?", ["Selecciona una opción", "Ver mi perfil", "Ver mis últimas actividades y subirlas a Firebase"])

        if opcion == "Ver mi perfil":
            fetch_athlete.get_athlete_data()

        elif opcion == "Ver mis últimas actividades y subirlas a Firebase":
            fetch_activities.get_activities() # Llama a la función modificada que sube a Firebase

    else:
        # 3. Si no hay código, mostramos el link para autorizar Strava
        st.warning("🔒 Necesitás conectar tu cuenta de Strava para continuar.")
        acc.getAuthorization()

if __name__ == "__main__":
    main()
    