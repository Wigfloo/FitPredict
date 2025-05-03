import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

# 1. Cargar los datos etiquetados
df = pd.read_csv("datos_etiquetados.csv")

# Limpiar los nombres de las columnas eliminando espacios en blanco al principio y al final
df.columns = df.columns.str.strip()

df['Fecha_actividad'] = pd.to_datetime(df['Fecha_actividad'])
df = df.sort_values(by=['ID_persona', 'Fecha_actividad'])

# 2. Definir la longitud de la secuencia de tiempo y las características
n_steps = 1060 # Considerar los últimos 70 entrenamientos
features = ['Frecuencia_cardiaca_prom', 'Ritmo_min_km', 'Distancia_metros']
n_features = len(features)
n_classes = 3  # elite, intermedio, novato

# 3. Agrupar y crear secuencias
grouped = df.groupby('ID_persona')
sequences = []
labels = []
for person_id, group in grouped:
    person_sequences = group[features].values
    person_labels = group['Perfil'].values  # Tomar las etiquetas de cada entrenamiento

    # Crear secuencias de longitud n_steps con padding si es necesario
    for i in range(max(0, len(person_sequences) - n_steps), len(person_sequences)):
        start_index = max(0, i - n_steps + 1)
        sequence = person_sequences[start_index:i+1]
        label = person_labels[i]  # Etiqueta correspondiente a esta secuencia

        if len(sequence) < n_steps:
            padding = np.zeros((n_steps - len(sequence), n_features))
            sequence = np.concatenate((padding, sequence))
        sequences.append(sequence)
        labels.append(label)

sequences = np.array(sequences)
labels = np.array(labels)

# 4. Codificar las etiquetas
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
y = to_categorical(encoded_labels, num_classes=n_classes)

# 5. Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(sequences, y, test_size=0.2, random_state=42, stratify=y)

# 6. Escalar las características
scaler = StandardScaler()
# Reshape para escalar cada característica individualmente a través de las secuencias
X_train_reshaped = X_train.reshape(-1, n_features)
X_test_reshaped = X_test.reshape(-1, n_features)
X_train_scaled = scaler.fit_transform(X_train_reshaped).reshape(X_train.shape)
X_test_scaled = scaler.transform(X_test_reshaped).reshape(X_test.shape)

# 7. Construir el modelo LSTM
model = Sequential()
model.add(LSTM(units=50, activation='relu', input_shape=(n_steps, n_features)))
model.add(Dense(units=n_classes, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# 8. Entrenar el modelo
model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test))

# 9. Evaluar el modelo
loss, accuracy = model.evaluate(X_test_scaled, y_test)
print(f'Loss: {loss:.4f}')
print(f'Accuracy: {accuracy:.4f}')