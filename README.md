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

📂 Estructura del Proyecto

```
A continuación, se presenta una visión general de la estructura de archivos y directorios más relevantes dentro del repositorio de FitPredict:

FitPredict/
├── app/
│   ├── main.py             # Punto de entrada principal de la aplicación Streamlit.
│   ├── auth.py             # Lógica relacionada con la autenticación de usuarios (Strava).
│   ├── requirements.txt    # Archivo que lista las dependencias necesarias para el proyecto.
│   └── models/             # Directorio que contiene los modelos de Machine Learning pre-entrenados.
│       ├── perfil.h5       # Modelo para el análisis de perfiles de usuario (si aplica).
│       ├── scaler.pkl      # Archivo con el scaler utilizado para preprocesar los datos del modelo.
│       ├── modelo_5k.pkl     # Modelo de Machine Learning para predicción de tiempos en carreras de 5k.
│       └── modelo_10k.pkl    # Modelo de Machine Learning para predicción de tiempos en carreras de 10k.
├── .env                    # Archivo para almacenar las variables de entorno (credenciales de Strava, etc.). Importante: No compartir.
├── README.md               # Este archivo, con la descripción general del proyecto.
└── ...                     # Otros archivos y directorios del proyecto.
```

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

---

## 12. Soporte y Comunidad

Dado que FitPredict es un proyecto de código abierto con la intención de ser utilizado y modificado libremente por la comunidad, el soporte técnico formal no está centralizado. Sin embargo, te invitamos a:

* **Reportar problemas y sugerir mejoras:** Utiliza la sección de [Issues](https://github.com/Wigfloo/FitPredict/issues) en el repositorio de GitHub para informar sobre cualquier error que encuentres o para proponer nuevas funcionalidades.
* **Contribuir al proyecto:** Si tienes habilidades de desarrollo, te animamos a realizar un fork del repositorio y enviar tus propias modificaciones a través de [Pull Requests](https://github.com/Wigfloo/FitPredict/pulls).
* **Interactuar con la comunidad:** Si se forma una comunidad alrededor del proyecto, podríamos considerar la creación de canales de comunicación como foros o salas de chat. Mantente atento al repositorio para futuras actualizaciones.

**En resumen, el soporte se basa en la colaboración y las contribuciones de la comunidad de código abierto.**

## 13. Glosario

Puedes mantener el glosario que ya creaste en el manual de usuario aquí en el README también, o hacer referencia a la documentación más completa si es muy extenso. Por ejemplo:

> Para un glosario de términos técnicos utilizados en este proyecto, por favor consulta la sección correspondiente en el [Manual de Usuario](link_al_manual_si_lo_tienes_aparte.md o #glosario-en-el-manual).

Si lo incluyes directamente en el README:

**Glosario:**

* **API (Application Programming Interface):** ... (tu definición)
* **Streamlit:** ... (tu definición)
* **Firebase (Firestore):** ... (tu definición)
* **Machine Learning (ML):** ... (tu definición)
* **OAuth:** ... (tu definición)
* **`REFRESH_TOKEN`:** ... (tu definición)
* **`ACCESS_TOKEN`:** ... (tu definición)
* **Entorno Virtual (venv):** ... (tu definición)
* **Repositorio (Git):** ... (tu definición)

## 14. Anexos (Opcional)**

Si tienes información adicional que pueda ser útil pero no encaja en las secciones principales, puedes incluirla aquí. Por ejemplo:

* **Contribución al Código:** Guías de estilo de código, proceso de envío de pull requests.
* **Licencia de Terceros:** Información sobre las licencias de las librerías que utilizas.

---

## 2. Código Software

El código fuente de FitPredict está disponible de forma abierta para que cualquiera pueda entender, reproducir, validar, usar y modificar el proyecto según los términos de la licencia adjunta.

### 1. Organización del Código

El código se organiza en los siguientes directorios principales:

* **`/app/`**: Contiene la lógica principal de la aplicación Streamlit.
    * `main.py`: Punto de entrada principal de la aplicación web.
    * `auth.py`: Maneja la autenticación con la API de Strava.
    * `requirements.txt`: Lista de dependencias necesarias para ejecutar la aplicación.
    * `/models/`: Almacena los modelos de Machine Learning pre-entrenados (`perfil.h5`, `scaler.pkl`, `modelo_5k.pkl`, `modelo_10k.pkl`).
* `.env`: Archivo para configurar variables de entorno sensibles (no rastreado por Git por seguridad).

### 2. Documentación del Código

* **`README.md`:** Este archivo proporciona una descripción general del proyecto, instrucciones de instalación y uso, requisitos del sistema, información de contacto y la licencia bajo la cual se distribuye el código.
* **Comentarios en el Código:** Se han incluido comentarios dentro del código fuente para explicar la lógica de las funciones, clases y secciones complejas.
* **Docstrings:** Las funciones y módulos importantes están documentados con docstrings para explicar su propósito, parámetros y valores de retorno (en el caso de Python).

### 3. Control de Versiones

El código de FitPredict se gestiona utilizando **Git** y se encuentra alojado en el repositorio de GitHub: [https://github.com/Wigfloo/FitPredict](https://github.com/Wigfloo/FitPredict). Te invitamos a explorar el historial de versiones, realizar forks del repositorio y contribuir con tus propias mejoras.

### 4. Licencia

Este proyecto se distribuye bajo la **[Elige aquí tu licencia de código abierto, por ejemplo: Licencia MIT](https://opensource.org/licenses/MIT)**.

Se adjunta un archivo `LICENSE` en la raíz del repositorio con los términos completos de esta licencia. Esta licencia permite a otros usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del software, sujeto a las condiciones establecidas en la licencia. **Al utilizar, modificar o distribuir este software, aceptas los términos de la licencia.**

---

## 👨‍💻 Autores

**George Ibañez Canchila (Wigfloo)**  
Estudiante de Ingeniería en Telecomunicaciones, amante del software libre, el desarrollo en Linux y el deporte.

**Matheo Enrique Herrera Zota**

Estudiante de Ingeniería en Telecomunicaciones, Amante al arte y al diseño de sotfware

---

Si te interesa el análisis deportivo con inteligencia artificial, ¡dale estrella y seguí el proyecto! ⭐
