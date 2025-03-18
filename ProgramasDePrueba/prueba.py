import requests

access_token = "35da7f966d306e9599574a9a26653ea0cc2c8c27"
url = "https://www.strava.com/api/v3/athlete"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)

print(response.json())  # Muestra los datos del atleta
