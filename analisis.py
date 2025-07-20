
import pandas as pd
import matplotlib.pyplot as plt

# 📥 Cargar datos desde la URL
url = "https://raw.githubusercontent.com/owid/co2-data/refs/heads/master/owid-co2-data.csv"
df = pd.read_csv(url)

# 🧼 Selección de columnas relevantes
columnas = ['country', 'year', 'iso_code', 'population', 'gdp', 'co2']
df = df[columnas]

# 🔍 Filtrar registros que corresponden a países (iso_code no vacío)
df = df[df['iso_code'].notna()]

# 🧯 Reemplazar valores nulos en co2 por cero
df['co2'] = df['co2'].fillna(0)

# 📊 Emisiones Totales acumuladas
emisiones_totales = df.groupby('country')['co2'].sum().sort_values(ascending=False).head(10)
print("🔟 Países con mayores emisiones acumuladas:")
print(emisiones_totales)

# 📆 Año más reciente del dataset
anio_reciente = df['year'].max()

# 📊 Emisiones en el último año
df_ultimo_anio = df[df['year'] == anio_reciente]
emisiones_ultimo_anio = df_ultimo_anio.groupby('country')['co2'].sum().sort_values(ascending=False).head(10)
print(f"\n🔟 Países con mayores emisiones en el año {anio_reciente}:")
print(emisiones_ultimo_anio)

# 📈 Emisiones per cápita
df['co2_per_capita'] = df['co2'] / df['population']
emisiones_per_capita = df[df['year'] == anio_reciente].sort_values(by='co2_per_capita', ascending=False).head(10)
print(f"\n🔟 Países con mayores emisiones per cápita en el año {anio_reciente}:")
print(emisiones_per_capita[['country', 'co2_per_capita']])

# 🌎 Evolución de emisiones de un país (ejemplo: Costa Rica)
pais = "Costa Rica"
df_pais = df[df['country'] == pais]
df_pais = df_pais[df_pais['year'] >= 1950]

# 📤 Crear carpeta de imágenes si no existe
import os
if not os.path.exists("img"):
    os.makedirs("img")

# 📊 Gráfico 1: Barras horizontales - Emisiones totales acumuladas
plt.figure(figsize=(10,6))
emisiones_totales.plot(kind='barh', color='teal')
plt.title("Emisiones acumuladas de CO₂ (Top 10 países)")
plt.xlabel("Millones de toneladas")
plt.ylabel("País")
plt.tight_layout()
plt.savefig("img/grafico_barras_total.png")
plt.close()

# 📊 Gráfico 2: Barras verticales - Emisiones en el último año
plt.figure(figsize=(10,6))
emisiones_ultimo_anio.plot(kind='bar', color='tomato')
plt.title(f"Emisiones de CO₂ en {anio_reciente} (Top 10 países)")
plt.ylabel("Millones de toneladas")
plt.xlabel("País")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("img/grafico_barras_ultimo.png")
plt.close()

# 📈 Gráfico 3: Línea - Evolución de país
plt.figure(figsize=(10,6))
plt.plot(df_pais['year'], df_pais['co2'], marker='o', linestyle='-', color='green')
plt.title(f"Evolución de emisiones de CO₂ en {pais} (1950 - {anio_reciente})")
plt.xlabel("Año")
plt.ylabel("Emisiones de CO₂")
plt.grid(True)
plt.tight_layout()
plt.savefig("img/grafico_linea_evolucion.png")
plt.close()

print("\n✅ Análisis y visualizaciones completadas. Archivos PNG guardados en la carpeta 'img'.")
