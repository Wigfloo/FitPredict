from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

# Cargar el DataFrame etiquetado (asegúrate de que 'etiquetar_datos.py' se haya ejecutado)
df = pd.read_csv("datos_etiquetados.csv")
df.columns = df.columns.str.strip() # Asegurarse de que los nombres de las columnas estén limpios

# Definir las características (X) y la variable objetivo (y)
X = df[['Ritmo_min_km', 'Distancia_metros', 'Frecuencia_cardiaca_prom', 'Edad', 'Sexo', 'IMC']]
y = df['Perfil']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Definir las columnas categóricas y numéricas
categorical_features = ['Sexo']
numerical_features = ['Ritmo_min_km', 'Distancia_metros', 'Frecuencia_cardiaca_prom', 'Edad', 'IMC']

# Crear un preprocesador utilizando ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Aplicar el preprocesador a los conjuntos de entrenamiento y prueba
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# Obtener los nombres de las columnas después del preprocesamiento (útil para DataFrame)
feature_names = numerical_features + list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features))

# Convertir los resultados procesados a DataFrames (opcional, pero útil para inspeccionar)
X_train_processed_df = pd.DataFrame(X_train_processed, columns=feature_names)
X_test_processed_df = pd.DataFrame(X_test_processed, columns=feature_names)

print("Conjunto de entrenamiento preprocesado:")
print(X_train_processed_df.head())
print("\nConjunto de prueba preprocesado:")
print(X_test_processed_df.head())