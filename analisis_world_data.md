# 🌍 Reporte de Análisis: Dataset World Data

Este documento detalla la estructura, puntos críticos, hallazgos interesantes y guías de visualización para el archivo `world_data.csv`.

---

## 1. 📊 Estructura del Dataset
El archivo contiene **195 registros** (países) con **17 columnas** que mezclan datos geográficos, demográficos y económicos.

### Columnas principales:
*   **Geografía:** `Country`, `Density (P/Km2)`, `Land Area(Km2)`, `Forested Area (%)`.
*   **Demografía:** `Birth Rate`, `Fertility Rate`.
*   **Economía:** `Gasoline Price`, `CPI`, `CPI Change (%)`, `Currency-Code`.
*   **Socio-Militar:** `Armed Forces size`, `Co2-Emissions`, `Agricultural Land( %)`.

---

## 2. 🔍 Puntos Importantes para el Análisis
Para un análisis de datos profundo (EDA), estos son los focos más relevantes:

1.  **Correlación Natalidad vs. Economía:** Relación entre el `Birth Rate` / `Fertility Rate` y los indicadores económicos.
2.  **Impacto Ambiental:** Comparar el `Forested Area (%)` frente a `Co2-Emissions`.
3.  **Uso de Suelo:** Analizar la competencia entre `Agricultural Land (%)` y `Forested Area (%)`.
4.  **Inflación y Estabilidad:** Uso de la columna `CPI Change (%)` para identificar volatilidad económica.

---

## 3. 🛠️ Retos de Exploración (Limpieza de Datos)
A nivel técnico, el archivo presenta varios desafíos:

*   **Formato de Strings:** Muchas columnas numéricas incluyen símbolos (`%`, `$`) y comas como separadores de miles que deben ser eliminados.
*   **Valores Nulos (NaN):** Columnas como `Gasoline Price`, `Armed Forces size` y `CPI` tienen datos faltantes significativos.
*   **Nombres de Columnas:** Algunas contienen saltos de línea (`\n`) o espacios extra (ej: `Birth Rate\n`).

---

## 4. ✨ Curiosidades y Hallazgos
*   **Contrastes de Gasolina:** Precios desde $0.28 (Argelia) hasta más de $1.50 en Europa.
*   **Inflación en Argentina:** Presenta un `CPI Change (%)` de 53.50%, destacando sobre el promedio.
*   **Densidad Extrema:** Grandes contrastes entre naciones isleñas/pequeñas y gigantes como Argelia (18 personas/Km2).
*   **Emisiones de CO2:** Disparidad masiva que revela niveles de industrialización muy variados entre países similares en tamaño.

---

## 5. 📈 Guía de Visualización

### Cómo hacer un Gráfico de Barras
Ideal para comparar magnitudes entre países (ej: Top 10 países con más bosques).

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('world_data.csv')
# Limpieza previa necesaria del símbolo %
df['Forested Area (%)'] = df['Forested Area (%)'].str.replace('%', '').astype(float)

top_bosques = df.nlargest(10, 'Forested Area (%)')
sns.barplot(x='Forested Area (%)', y='Country', data=top_bosques, palette='viridis')
plt.title('Top 10 Países con mayor superficie forestal (%)')
plt.show()
```

### Cómo hacer un Mapa de Calor (Heatmap)
Usado para ver la correlación entre variables numéricas.

```python
# Seleccionamos variables de interés
columnas_interes = ['Birth Rate', 'Fertility Rate', 'Co2-Emissions', 'Forested Area (%)']
matriz_correlacion = df[columnas_interes].corr()

sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlación entre indicadores mundiales')
plt.show()
```
