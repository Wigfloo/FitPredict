import requests

client_id = "150300"
client_secret = "e16beb9a5c81bef53101a84111d87a55f6a41f13"
auth_code = "f228c2c89b4656e798fdf7d76c80107f1324d18f"

url = "https://www.strava.com/api/v3/oauth/token"
payload = {
    "client_id": client_id,
    "client_secret": client_secret,
    "code": auth_code,
    "grant_type": "authorization_code"
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    tokens = response.json()
    print("Access Token:", tokens["access_token"])
    print("Refresh Token:", tokens["refresh_token"])
else:
    print("Error:", response.json())
