import requests

# Token de acceso obtenido antes
access_token = "35da7f966d306e9599574a9a26653ea0cc2c8c27"

# URL del endpoint de actividades
url = "https://www.strava.com/api/v3/athlete/activities"

# Encabezados de la petición
headers = {"Authorization": f"Bearer {access_token}"}

# Hacer la petición
response = requests.get(url, headers=headers)

# Imprimir la respuesta
if response.status_code == 200:
    actividades = response.json()
    print("Entrenamientos obtenidos:")
    for actividad in actividades[:5]:  # Mostramos solo las primeras 5 actividades
        print(f"- {actividad['name']} | Distancia: {actividad['distance']} metros | Duración: {actividad['moving_time']} segundos")
else:
    print(f"Error al obtener actividades: {response.status_code} - {response.text}")
