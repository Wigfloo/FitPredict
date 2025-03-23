import os
import requests
from flask import Flask, request

CLIENT_ID = "150300"  # Tu Client ID de Strava
CLIENT_SECRET = "e16beb9a5c81bef53101a84111d87a55f6a41f13"  # Tu Client Secret de Strava
REDIRECT_URI = "http://localhost:5000/exchange_token"

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor Flask corriendo. Usa /authorize para autenticarte con Strava."

@app.route("/authorize")
def authorize():
    url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=read,activity:read_all"
    return f'<a href="{url}">Autenticarse con Strava</a>'

@app.route("/exchange_token")
def exchange_token():
    code = request.args.get("code")
    if not code:
        return "Error: No se recibió el código de autorización.", 400

    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=payload)
    return response.json()

if __name__ == "__main__":
    app.run(port=5000)
