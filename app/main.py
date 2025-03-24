import auth
import fetch_athlete
import fetch_activities
import streamlit as st
import acces_code as acc

#crear ruta de navegacion ,menu 
def main():
    # Validamos que el usuario tenga una sesion activa
    if auth.checkAuthorization():
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
    else:
        acc.getAuthorization()

if __name__ == "__main__":
    main()
