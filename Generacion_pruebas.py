import random
import pandas as pd
import numpy as np

# ---------- Generación de personas ----------
def generar_datos_personas(n=1000):
    personas = []
    perfiles = [0, 1, 2] * ((n // 3) + 1)
    random.shuffle(perfiles)

    for i in range(n):
        sexo = random.choice(['M', 'F'])
        edad = random.randint(18, 50)

        if sexo == 'M':
            peso = round(random.uniform(65, 90), 1)
            altura = round(random.uniform(1.70, 1.90), 2)
        else:
            peso = round(random.uniform(50, 70), 1)
            altura = round(random.uniform(1.55, 1.75), 2)

        imc = round(peso / (altura ** 2), 2)

        persona = {
            'ID_persona': f'P{i:03d}',
            'Sexo': sexo,
            'Edad': edad,
            'Peso_kg': peso,
            'Altura_m': altura,
            'IMC': imc,
            'perfil': perfiles[i]  # 0 = elite, 1 = intermedio, 2 = novato
        }

        personas.append(persona)

    return personas

# ---------- Prueba de 3000m ----------
def generar_datos_3000m(personas):
    datos = []
    factores_ritmo = {
        0: {'5k': 1.03, '10k': 1.06},  # Élite
        1: {'5k': 1.05, '10k': 1.09},  # Intermedio
        2: {'5k': 1.07, '10k': 1.12}   # Novato
    }
    for persona in personas:
        perfil = persona['perfil']
        edad = persona['Edad']
        sexo = persona['Sexo']

        # Introducir una pequeña variación en la distancia real de la prueba
        distancia_real_m = round(random.uniform(2950, 3050), 0)

        if perfil == 0:
            ritmo_base_3k = round(random.uniform(3.3, 3.8), 2)
            fc_prom_3k = random.randint(145, 160)
        elif perfil == 1:
            ritmo_base_3k = round(random.uniform(4.5, 5.8), 2)
            fc_prom_3k = random.randint(155, 170)
        else:
            ritmo_base_3k = round(random.uniform(6.5, 8.0), 2)
            fc_prom_3k = random.randint(165, 185)

        # Calculamos el tiempo basado en el ritmo base y la distancia REAL
        tiempo_3k_seg = int(ritmo_base_3k * distancia_real_m / 1000 * 60)
        ritmo_promedio_3k = tiempo_3k_seg / (distancia_real_m / 1000) / 60 if distancia_real_m > 0 else np.nan
        velocidad_3k_mps = distancia_real_m / tiempo_3k_seg if tiempo_3k_seg > 0 else np.nan
        fc_max_teorica = 226 - edad if sexo == 'F' else 220 - edad
        fc_max_3k = min(fc_max_teorica + random.randint(-2, 5), 200)

        minutos_3k = int(ritmo_promedio_3k) if not np.isnan(ritmo_promedio_3k) else 0
        segundos_3k = int((ritmo_promedio_3k - minutos_3k) * 60) if not np.isnan(ritmo_promedio_3k) else 0
        ritmo_3k_formato = f"{minutos_3k}:{segundos_3k:02d}" if not np.isnan(ritmo_promedio_3k) else "N/A"

        # Estimación para 5k (usando el ritmo PROMEDIO del 3k)
        factor_5k = factores_ritmo[perfil]['5k']
        ritmo_5k = round(ritmo_promedio_3k * factor_5k, 2) if not np.isnan(ritmo_promedio_3k) else np.nan
        tiempo_5k_seg = int(ritmo_5k * 5 * 60) if not np.isnan(ritmo_5k) else np.nan
        fc_prom_5k = int(fc_prom_3k + random.randint(-5, 5))

        minutos_5k = int(ritmo_5k) if not np.isnan(ritmo_5k) else 0
        segundos_5k = int((ritmo_5k - minutos_5k) * 60) if not np.isnan(ritmo_5k) else 0
        ritmo_5k_formato = f"{minutos_5k}:{segundos_5k:02d}" if not np.isnan(ritmo_5k) else "N/A"

        # Estimación para 10k (usando el ritmo PROMEDIO del 3k)
        factor_10k = factores_ritmo[perfil]['10k']
        ritmo_10k = round(ritmo_promedio_3k * factor_10k, 2) if not np.isnan(ritmo_promedio_3k) else np.nan
        tiempo_10k_seg = int(ritmo_10k * 10 * 60) if not np.isnan(ritmo_10k) else np.nan
        fc_prom_10k = int(fc_prom_3k + random.randint(-10, 0))

        minutos_10k = int(ritmo_10k) if not np.isnan(ritmo_10k) else 0
        segundos_10k = int((ritmo_10k - minutos_10k) * 60) if not np.isnan(ritmo_10k) else 0
        ritmo_10k_formato = f"{minutos_10k}:{segundos_10k:02d}" if not np.isnan(ritmo_10k) else "N/A"

        datos.append({
            'ID_persona': persona['ID_persona'],
            'Sexo': sexo,
            'Edad': edad,
            'Peso_kg': persona['Peso_kg'],
            'Altura_m': persona['Altura_m'],
            'IMC': persona['IMC'],
            'Distancia_3k_real_m': distancia_real_m,
            'Tiempo_3k_seg': tiempo_3k_seg,
            'Ritmo_3k_min_km': ritmo_promedio_3k,
            'Ritmo_3k_formato': ritmo_3k_formato,
            'Velocidad_3k_mps': round(velocidad_3k_mps, 2) if not np.isnan(velocidad_3k_mps) else np.nan,
            'Frecuencia_cardiaca_prom_3k': fc_prom_3k,
            'Frecuencia_cardiaca_max_3k': fc_max_3k,
            'Tiempo_5k_seg_estimado': tiempo_5k_seg,
            'Ritmo_5k_min_km_estimado': ritmo_5k,
            'Ritmo_5k_formato_estimado': ritmo_5k_formato,
            'Frecuencia_cardiaca_prom_5k_estimado': fc_prom_5k,
            'Tiempo_10k_seg_estimado': tiempo_10k_seg,
            'Ritmo_10k_min_km_estimado': ritmo_10k,
            'Ritmo_10k_formato_estimado': ritmo_10k_formato,
            'Frecuencia_cardiaca_prom_10k_estimado': fc_prom_10k
        })
    return datos

# ---------- Prueba de 20 minutos (sin cambios por ahora) ----------
def generar_datos_20min(personas):
    datos = []
    duracion_seg = 20 * 60
    for persona in personas:
        perfil = persona['perfil']
        edad = persona['Edad']
        sexo = persona['Sexo']

        if perfil == 0:
            ritmo_min_km = round(random.uniform(3.3, 4.0), 2)
            fc_prom = random.randint(160, 175)
        elif perfil == 1:
            ritmo_min_km = round(random.uniform(5.0, 6.0), 2)
            fc_prom = random.randint(165, 180)
        else:
            ritmo_min_km = round(random.uniform(6.5, 8.5), 2)
            fc_prom = random.randint(170, 190)

        velocidad_mps = 1000 / (ritmo_min_km * 60)
        distancia = round(velocidad_mps * duracion_seg)
        fc_max_teorica = 226 - edad if sexo == 'F' else 220 - edad
        fc_max = min(fc_max_teorica + random.randint(0, 10), 200)

        minutos = int(ritmo_min_km)
        segundos = int((ritmo_min_km - minutos) * 60)
        ritmo_formateado = f"{minutos}:{segundos:02d}"

        datos.append({
            'ID_persona': persona['ID_persona'],
            'Sexo': sexo,
            'Edad': edad,
            'Peso_kg': persona['Peso_kg'],
            'Altura_m': persona['Altura_m'],
            'IMC': persona['IMC'],
            'Duracion_min': 20,
            'Distancia_m': distancia,
            'Ritmo_min_km': ritmo_min_km,
            'Ritmo_formato': ritmo_formateado,
            'Velocidad_mps': round(velocidad_mps, 2),
            'Frecuencia_cardiaca_prom': fc_prom,
            'Frecuencia_cardiaca_max': fc_max
        })
    return datos

# ---------- Generar y guardar ----------
personas = generar_datos_personas(1000)
df_3000m_variado = pd.DataFrame(generar_datos_3000m(personas))
df_20min = pd.DataFrame(generar_datos_20min(personas))

df_3000m_variado.to_csv("prueba_3000m_con_variacion.csv", index=False)
df_20min.to_csv("prueba_20min.csv", index=False)

print("Datos de la prueba de 3000m con variación en la distancia generados y guardados en prueba_3000m_con_variacion.csv")
print("Datos de la prueba de 20 minutos generados y guardados en prueba_20min.csv")
print(df_3000m_variado.head())