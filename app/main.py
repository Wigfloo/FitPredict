import auth
import fetch_athlete
import fetch_activities

def main():
    print("\n🏃‍♂️ Bienvenido a Strava CLI!")
    print("1. Ver mi perfil")
    print("2. Ver mis últimas actividades")
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        fetch_athlete.get_athlete_data()
    elif opcion == "2":
        fetch_activities.get_activities()
    else:
        print("❌ Opción inválida.")

if __name__ == "__main__":
    auth.refresh_access_token()  # Asegurar que el token esté actualizado
    main()
