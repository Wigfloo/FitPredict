import requests
import config

def get_activities():
    """Obtiene y muestra las 5 actividades más recientes del atleta"""
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {config.ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        activities = response.json()
        print("✅ Actividades obtenidas:")
        for i, activity in enumerate(activities[:5]):
            print(f"{i+1}. {activity['name']} - {activity['distance']} metros")
    else:
        print("❌ Error al obtener actividades:", response.status_code)
        print(response.json())

# Llamar la función cuando se necesite
# get_activities()
