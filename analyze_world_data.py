import pandas as pd
import numpy as np

# Cargar datos
df = pd.read_csv('world_data.csv')

# Funciones de limpieza
def clean_pct(x):
    if pd.isnull(x) or str(x).lower() == 'nan':
        return np.nan
    return float(str(x).replace('%', '').replace(',', '').strip())

def clean_num(x):
    if pd.isnull(x) or str(x).lower() == 'nan':
        return np.nan
    # Manejar posibles strings vacíos
    val = str(x).replace(',', '').replace('$', '').strip()
    if not val:
        return np.nan
    try:
        return float(val)
    except ValueError:
        return np.nan

# Aplicar limpieza
df['Density'] = df['Density\n(P/Km2)'].apply(clean_num)
df['Agri_Land'] = df['Agricultural Land( %)'].apply(clean_pct)
df['Land_Area'] = df['Land Area(Km2)'].apply(clean_num)
df['Armed_Forces'] = df['Armed Forces size'].apply(clean_num)
df['Birth_Rate'] = df['Birth Rate\n'].apply(clean_num)
df['CO2'] = df['Co2-Emissions'].apply(clean_num)
df['Forested'] = df['Forested Area (%)'].apply(clean_pct)
df['Gas_Price'] = df['Gasoline Price'].apply(clean_num)
df['CPI_Change'] = df['CPI Change (%)'].apply(clean_pct)

# Análisis general
print("--- RESUMEN ESTADÍSTICO ---")
print(df[['Density', 'Birth_Rate', 'Fertility Rate', 'Agri_Land', 'Forested', 'Gas_Price', 'CO2', 'CPI_Change']].describe())

# Curiosidades
print("\n--- CURIOSIDADES ---")

# Países más boscosos
top_forested = df.nlargest(5, 'Forested')[['Country', 'Forested']]
print("\nTop 5 Países más boscosos (%):")
print(top_forested.to_string(index=False))

# Países con gasolina más barata y más cara
top_gas = df.nlargest(3, 'Gas_Price')[['Country', 'Gas_Price']]
bottom_gas = df.nsmallest(3, 'Gas_Price')[['Country', 'Gas_Price']]
print("\nGasolina más cara ($):")
print(top_gas.to_string(index=False))
print("\nGasolina más barata ($):")
print(bottom_gas.to_string(index=False))

# CO2 vs Tamaño (pista de ineficiencia)
df['CO2_per_Km2'] = df['CO2'] / df['Land_Area']
top_co2_density = df.nlargest(5, 'CO2_per_Km2')[['Country', 'CO2_per_Km2']]
print("\nTop 5 Emisiones CO2 por Km2 (densidad de contaminación):")
print(top_co2_density.to_string(index=False))

# Natalidad vs Fertilidad
print("\nCorrelación Natalidad-Fertilidad:", df['Birth_Rate'].corr(df['Fertility Rate']))

# Datos faltantes
print("\n--- DATOS FALTANTES ---")
print(df.isnull().sum())
