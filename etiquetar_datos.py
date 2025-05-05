import pandas as pd

# Cargar el DataFrame que guardaste
df = pd.read_csv("datos_corredores.csv")

# Limpiar los nombres de las columnas eliminando espacios en blanco
df.columns = df.columns.str.strip()

def etiquetar_perfil(row):
    """
    Etiqueta el perfil de un corredor basado en sus características de entrenamiento.
    Devuelve 'elite', 'intermedio' o 'novato'.
    Devuelve None para los datos que no encajan claramente en estas categorías.
    """
    ritmo = row['Ritmo_min_km']
    distancia = row['Distancia_metros']
    fc_prom = row['Frecuencia_cardiaca_prom']

    # Rangos definidos en tu script de generación (ajusta si los modificaste)
    ritmo_elite = (3.5, 4.2)
    distancia_elite = (10000, 20000)
    fc_elite = (135, 155)

    ritmo_intermedio = (5.0, 6.5)
    distancia_intermedio = (6000, 12000)
    fc_intermedio = (145, 165)

    ritmo_novato = (7.0, 9.0)
    distancia_novato = (3000, 8000)
    fc_novato = (155, 175)

    # Lógica de etiquetado
    if (ritmo_elite[0] <= ritmo <= ritmo_elite[1] and
        distancia >= distancia_elite[0] and
        fc_elite[0] <= fc_prom <= fc_elite[1]):
        return 'elite'
    elif (ritmo_intermedio[0] <= ritmo <= ritmo_intermedio[1] and
          distancia >= distancia_intermedio[0] and
          fc_intermedio[0] <= fc_prom <= fc_intermedio[1]):
        return 'intermedio'
    elif (ritmo_novato[0] <= ritmo <= ritmo_novato[1] and
          distancia >= distancia_novato[0] and
          fc_novato[0] <= fc_prom <= fc_novato[1]):
        return 'novato'
    else:
        return None  # Ya no devolvemos 'desconocido'

# Aplicar la función de etiquetado al DataFrame
df['Perfil'] = df.apply(etiquetar_perfil, axis=1)

# Eliminar las filas donde la etiqueta 'Perfil' es None
df_filtrado = df.dropna(subset=['Perfil'])

# Guardar el DataFrame filtrado con las etiquetas
df_filtrado.to_csv("datos_etiquetados.csv", index=False)

print("DataFrame con etiquetas (sin 'desconocido') guardado en datos_etiquetados.csv")