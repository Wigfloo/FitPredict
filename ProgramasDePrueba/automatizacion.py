import os
import datos
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

url = "https://www.strava.com/oauth/token"

params = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN
}

response = requests.post(url, data=params)

if response.status_code == 200:
    new_tokens = response.json()
    print("✅ Access Token Renovado:")
    print(new_tokens["access_token"])
else:
    print(f"❌ Error al renovar token: {response.status_code}")
    print(response.json())
