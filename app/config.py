import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = ''
URL_API = os.getenv("URL_API")

# Inicialmente, no hay un access token, se actualizará en automatizacion.py
ACCESS_TOKEN = None
