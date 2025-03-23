import requests

ACCESS_TOKEN = "f5c81b30fbec1460879ae103307a56ab0ce632e5"

url = "https://www.strava.com/api/v3/athlete"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ Datos del atleta:")
    print(response.json())
else:
    print(f"❌ Error: {response.status_code}")
    print(response.json())
