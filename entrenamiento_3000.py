import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# 1. Cargar el NUEVO Dataset
df = pd.read_csv("prueba_3000m_con_variacion.csv")

# Limpiar los nombres de las columnas eliminando espacios en blanco
df.columns = df.columns.str.strip()

# 2. Preprocesamiento de Datos
# Codificación de la variable 'Sexo'
label_encoder = LabelEncoder()
df['Sexo_encoded'] = label_encoder.fit_transform(df['Sexo'])

# Selección de Características (X)
features = [
    'Ritmo_3k_min_km',
    'Frecuencia_cardiaca_prom_3k',
    'Frecuencia_cardiaca_max_3k',
    'Sexo_encoded',
    'Edad',
    'IMC'
]
X = df[features]

# Selección de Etiquetas (y)
labels_5k = [
    'Ritmo_5k_min_km_estimado',
    'Tiempo_5k_seg_estimado',
    'Frecuencia_cardiaca_prom_5k_estimado'
]
y_5k = df[labels_5k]

labels_10k = [
    'Ritmo_10k_min_km_estimado',
    'Tiempo_10k_seg_estimado',
    'Frecuencia_cardiaca_prom_10k_estimado'
]
y_10k = df[labels_10k]

# Escalado de Características Numéricas
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# División de Datos en Entrenamiento y Prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_5k_train, y_5k_test, y_10k_train, y_10k_test = train_test_split(
    X_scaled, y_5k, y_10k, test_size=0.2, random_state=42
)

# 3. Selección y Entrenamiento del Modelo (Random Forest Regressor)

# Modelo para predecir 5k
rf_model_5k = RandomForestRegressor(random_state=42)
rf_model_5k.fit(X_train, y_5k_train)

# Modelo para predecir 10k
rf_model_10k = RandomForestRegressor(random_state=42)
rf_model_10k.fit(X_train, y_10k_train)

# 4. Evaluación del Modelo
# Predicciones en el conjunto de prueba
y_5k_pred = rf_model_5k.predict(X_test)
y_10k_pred = rf_model_10k.predict(X_test)

# Evaluación para 5k
mse_5k = mean_squared_error(y_5k_test, y_5k_pred)
r2_5k = r2_score(y_5k_test, y_5k_pred)
print("\n--- Resultados del Modelo para 5k (Re-entrenado) ---")
print(f"Error Cuadrático Medio (MSE): {mse_5k:.2f}")
print(f"Coeficiente de Determinación (R^2): {r2_5k:.2f}")

# Evaluación para 10k
mse_10k = mean_squared_error(y_10k_test, y_10k_pred)
r2_10k = r2_score(y_10k_test, y_10k_pred)
print("\n--- Resultados del Modelo para 10k (Re-entrenado) ---")
print(f"Error Cuadrático Medio (MSE): {mse_10k:.2f}")
print(f"Coeficiente de Determinación (R^2): {r2_10k:.2f}")

# 5. Guardar los Modelos y el Scaler (Sobrescribiendo los archivos anteriores)
with open('modelo_5k.pkl', 'wb') as file:
    pickle.dump(rf_model_5k, file)

with open('modelo_10k.pkl', 'wb') as file:
    pickle.dump(rf_model_10k, file)

with open('scaler_3k_pred.pkl', 'wb') as file:
    pickle.dump(scaler, file)

with open('label_encoder_sexo.pkl', 'wb') as file:
    pickle.dump(label_encoder, file)

print("\nModelos y scaler re-entrenados y guardados exitosamente!")