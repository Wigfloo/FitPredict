# 🏃‍♂️ FitPredict - Análisis Inteligente de Rendimiento Deportivo

**FitPredict** es una aplicación desarrollada con Python y Streamlit que permite a atletas de carreras de larga distancia conectar su cuenta de **Strava**, visualizar sus entrenamientos y analizar su rendimiento a través de modelos de Machine Learning.

---

## 📦 Tecnologías y librerías utilizadas

- **Python 3.11**
- **Streamlit**: interfaz web interactiva y ligera
- **Firebase (Firestore)**: almacenamiento de datos en la nube
- **MongoDB** (opcional): almacenamiento local o remoto de datos estructurados
- **pandas**: manipulación de datos
- **requests**: peticiones HTTP a la API de Strava
- **python-dotenv**: manejo de variables de entorno
- **Flask** (en versiones previas del flujo de autorización)

---

## 🧠 Características principales

- Conexión directa a la cuenta de Strava del usuario
- Obtención automática de todas las actividades deportivas
- Almacenamiento de datos relevantes en Firestore para análisis posterior
- Visualización y organización de entrenamientos por distancia, duración, fecha, etc.
- Modelo de Machine Learning para predecir el rendimiento del usuario (en construcción)

> Los datos utilizados para entrenar el modelo fueron obtenidos de bases de datos deportivas disponibles públicamente en internet.

---

## 🗂 Estructura del proyecto


* **`/app/`**: Contiene la lógica principal de la aplicación.
    * `main.py`: El script principal que ejecuta la aplicación Streamlit.
    * `auth.py`: Maneja la autenticación y conexión con la API de Strava.
    * `requirements.txt`: Lista todas las librerías de Python necesarias para que la aplicación funcione. Debes instalar estas dependencias usando `pip install -r requirements.txt`.
    * `/models/`: Almacena los modelos de Machine Learning pre-entrenados utilizados para el análisis y la predicción.
        * `perfil.h5`: (Si aplica) Modelo para analizar características del perfil de usuario.
        * `scaler.pkl`: Archivo que contiene el objeto `scaler` utilizado para normalizar o estandarizar los datos antes de ser introducidos en los modelos.
        * `modelo_5k.pkl`: Modelo entrenado para predecir el tiempo en carreras de 5 kilómetros.
        * `modelo_10k.pkl`: Modelo entrenado para predecir el tiempo en carreras de 10 kilómetros.
* `.env`: Archivo donde se guardan las variables de entorno sensibles, como tus credenciales de la API de Strava. **Este archivo no debe compartirse públicamente.**
* `README.md`: El archivo que estás leyendo, que proporciona una descripción general del proyecto, instrucciones de instalación y uso, entre otra información relevante.



---

## 🔐 Variables de entorno necesarias (`.env` o `config.py`)

```env
CLIENT_ID=tu_client_id_de_strava
CLIENT_SECRET=tu_client_secret_de_strava
REFRESH_TOKEN=tu_refresh_token
ACCESS_TOKEN=tu_access_token_inicial
URL_API=https://www.strava.com/api/v3
```

---

## 🚀 Cómo ejecutar el proyecto localmente

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Wigfloo/FitPredict.git
   cd FitPredict
   ```

2. Crear un entorno virtual en app/:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar la app:
   ```bash
   streamlit run app/main.py
   ```

---

## 📋 Estado del proyecto

- [x] Conexión con Strava
- [x] Sincronización y almacenamiento de entrenamientos
- [x] Visualización en Streamlit
- [x] Entrenamiento del modelo de predicción

---

## 👨‍💻 Autores

**George Ibañez Canchila (Wigfloo)**  
Estudiante de Ingeniería en Telecomunicaciones, amante del software libre, el desarrollo en Linux y el deporte.

**Matheo Enrique Herrera Zota**

Estudiante de Ingeniería en Telecomunicaciones, Amante al arte y al diseño de sotfware

---

Si te interesa el análisis deportivo con inteligencia artificial, ¡dale estrella y seguí el proyecto! ⭐
