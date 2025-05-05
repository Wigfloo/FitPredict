import random
import pandas as pd
from datetime import datetime, timedelta

# ---------- Datos personales ----------
def generar_datos_personas(n=10):
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
            'Peso': peso,
            'Altura': altura,
            'IMC': imc,
            'perfil': perfiles[i]  # 0 = elite, 1 = intermedio, 2 = novato
        }

        personas.append(persona)

    return personas

# ---------- Fechas aleatorias ----------
def generar_fechas_random_año(num_fechas):
    inicio = datetime(2024, 1, 1)
    fin = datetime(2024, 12, 31)
    dias_totales = (fin - inicio).days
    fechas = random.sample(
        [inicio + timedelta(days=i) for i in range(dias_totales)],
        num_fechas
    )
    return sorted(fechas)

# ---------- Generación de datos de entrenamiento ----------
personas_info = generar_datos_personas(10)
datos = []

for idx, persona in enumerate(personas_info):
    id_persona = persona['ID_persona']
    edad = persona['Edad']
    sexo = persona['Sexo']
    peso = persona['Peso']
    altura = persona['Altura']
    imc = persona['IMC']
    perfil = persona['perfil']

    cantidad_entrenos = random.randint(100, 150)
    fechas = generar_fechas_random_año(cantidad_entrenos)

    fc_max_teorica = 226 - edad if sexo == 'F' else 220 - edad
    fc_reposo = random.randint(40, 50) if perfil == 0 else random.randint(45, 60)

    if perfil == 0:  # elite
        ritmo_range = (3.5, 4.2)
        distancia_range = (10000, 20000)
        fc_range_inicial = (135, 155)
        mejora_fc = 3
        mejora_ritmo = 0.005
    elif perfil == 1:  # intermedio
        ritmo_range = (5.0, 6.5)
        distancia_range = (6000, 12000)
        fc_range_inicial = (145, 165)
        mejora_fc = 8
        mejora_ritmo = 0.03
    else:  # novato
        ritmo_range = (7.0, 9.0)
        distancia_range = (3000, 8000)
        fc_range_inicial = (155, 175)
        mejora_fc = 12
        mejora_ritmo = 0.07

    for i, fecha in enumerate(fechas):
        progreso = i / len(fechas)  # de 0 a 1

        # Menor variabilidad en el ritmo para la élite
        if perfil == 0:
            ritmo_min_km = round(random.uniform(ritmo_range[0] + 0.1, ritmo_range[1] - 0.1), 2)
        else:
            ritmo_min_km = round(random.uniform(*ritmo_range), 2)

        distancia = random.randint(*distancia_range)
        tiempo = int((ritmo_min_km * distancia) / 1000 * 60)
        tiempo = int(tiempo * (1 - progreso * mejora_ritmo))
        tiempo = max(tiempo, 900)

        velocidad = distancia / tiempo
        minutos = int(ritmo_min_km)
        segundos = int((ritmo_min_km - minutos) * 60)
        ritmo_formateado = f"{minutos}:{segundos:02d}"

        fc_max = random.randint(fc_max_teorica - 5, fc_max_teorica + 5)

        # Calcular FC promedio realista
        fc_prom_inicial = random.randint(*fc_range_inicial)
        fc_prom_mejorada = fc_prom_inicial - int(progreso * mejora_fc)
        fc_prom = max(fc_prom_mejorada, fc_reposo + 15 if perfil == 0 else fc_reposo + 25) # Ajuste del margen

        horas = tiempo // 3600
        minutos_tiempo = (tiempo % 3600) // 60
        tiempo_formato = f"{int(horas)}:{int(minutos_tiempo):02d}"

        datos.append({
            'ID_persona': id_persona,
            'Sexo': sexo,
            'Edad': edad,
            'Peso_kg': peso,
            'Altura_m': altura,
            'IMC': imc,
            'Fecha_actividad': fecha.strftime('%Y-%m-%d'),
            'Tiempo_segundos': tiempo,
            'Tiempo_horas': tiempo_formato,
            'Distancia_metros': distancia,
            'Ritmo_min_km': ritmo_min_km,
            'Ritmo_formato': ritmo_formateado,
            'Frecuencia_cardiaca_max': fc_max,
            'Frecuencia_cardiaca_prom': fc_prom,
            'Frecuencia_cardiaca_reposo': fc_reposo,
            'Velocidad_promedio_mps': round(velocidad, 2),
        })

df = pd.DataFrame(datos)
df.to_csv("datos_corredores2.csv", index=False)
df.head(10)