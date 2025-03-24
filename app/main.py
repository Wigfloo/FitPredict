import auth
import fetch_athlete
import fetch_activities
import streamlit as st

def main():
    st.write("\n🏃‍♂️ Bienvenido a Strava CLI!")
    st.write("1. Ver mi perfil")
    st.write("2. Ver mis últimas actividades")
    opcion = st.text_input("Selecciona una opción: ", key="opcion")

    if opcion == "1":
        st.write(fetch_athlete.get_athlete_data())
    elif opcion == "2":
       st.write( fetch_activities.get_activities())
    else:
        st.write("❌ Opción inválida.")

if __name__ == "__main__":
    auth.refresh_access_token()  # Asegurar que el token esté actualizado
    main()
