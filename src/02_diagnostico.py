"""
Diagnóstico de calidad y cobertura de datos
"""
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_RAW, DATASET_NAME

df = pd.read_excel(DATA_RAW / DATASET_NAME)

print("=== DIMENSIONES ===")
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}\n")

print("=== COBERTURA POR COLUMNA (% datos no nulos) ===")
cobertura = (df.notna().sum() / len(df) * 100).round(2).sort_values(ascending=False)
print(cobertura.to_string())

print("\n=== AÑOS DISPONIBLES ===")
print(f"Min: {df['year'].min()} | Max: {df['year'].max()}")
print(f"Registros por año (últimos 20):")
print(df['year'].value_counts().sort_index().tail(20))

print("\n=== COLUMNAS CON MÁS DEL 50% DE DATOS ===")
cols_ok = cobertura[cobertura > 50].index.tolist()
print(f"Total: {len(cols_ok)} columnas")
for c in cols_ok:
    print(f"  - {c}")

print("\n=== REGISTROS CON DATOS DE POBREZA INFANTIL ===")
cols_pobreza = [c for c in df.columns if 'child_poverty' in c]
if cols_pobreza:
    df_pob = df.dropna(subset=cols_pobreza, how='all')
    print(f"Filas con al menos 1 dato de pobreza infantil: {len(df_pob)}")
    print(f"Países únicos: {df_pob['country_name'].nunique()}")
    print(f"Rango de años: {df_pob['year'].min()} - {df_pob['year'].max()}")
