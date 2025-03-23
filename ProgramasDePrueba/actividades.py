import requests

ACCESS_TOKEN = "f5c81b30fbec1460879ae103307a56ab0ce632e5"

url = "https://www.strava.com/api/v3/athlete/activities"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    activities = response.json()
    print("✅ Actividades obtenidas:")
    for i, activity in enumerate(activities[:5]):  # Muestra solo las primeras 5
        print(f"{i+1}. {activity['name']} - {activity['distance']} metros")
else:
    print(f"❌ Error al obtener actividades: {response.status_code}")
    print(response.json())
