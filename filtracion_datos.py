import pandas as pd

# Cargar datos
df = pd.read_csv("datos_corredores2.csv")
df.columns = df.columns.str.strip()  # Esto limpia TODOS los nombres de columnas

# Convertir segundos a minutos para filtrar prueba de 20 min
df['Duracion_min'] = df['Tiempo_segundos'] / 60

# Almacenamos los datos finales
datos_modelo = []

for persona_id in df['ID_persona'].unique():
    persona_df = df[df['ID_persona'] == persona_id]
    perfil = persona_df['perfil'].values[0]  # Obtener el perfil real de la persona

    # Buscar actividad de 20 minutos (±2 min)
    prueba_20min = persona_df[(persona_df['Duracion_min'] >= 18) & (persona_df['Duracion_min'] <= 22)]
    # Buscar actividad de 3000m (±200m)
    prueba_3k = persona_df[(persona_df['Distancia_metros'] >= 2800) & (persona_df['Distancia_metros'] <= 3200)]

    if not prueba_20min.empty and not prueba_3k.empty:
        act_20min = prueba_20min.sample(1).iloc[0]
        act_3k = prueba_3k.sample(1).iloc[0]

        datos_modelo.append({
            'ritmo_20min': act_20min['Ritmo_min_km'],
            'fc_prom_20min': act_20min['Frecuencia_cardiaca_prom'],
            'fc_max_20min': act_20min['Frecuencia_cardiaca_max'],

            'ritmo_3k': act_3k['Ritmo_min_km'],
            'fc_prom_3k': act_3k['Frecuencia_cardiaca_prom'],
            'fc_max_3k': act_3k['Frecuencia_cardiaca_max'],

            'Edad': act_3k['Edad'],  # puedes agregar más si quieres
            'IMC': act_3k['IMC'],

            'perfil': perfil
        })

# Crear DataFrame
df_modelo = pd.DataFrame(datos_modelo)
df_modelo.to_csv("dataset_entrenamiento_modelo1.csv", index=False)
print(df_modelo.head())
