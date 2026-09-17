"""
Paso 2: Importación y exploración inicial del dataset (Excel)
"""
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_RAW, DATASET_NAME

# Importar dataset Excel
ruta = DATA_RAW / DATASET_NAME
print(f"Cargando: {ruta}\n")

# Leer todas las hojas del Excel
xls = pd.ExcelFile(ruta)
print(f"Hojas disponibles: {xls.sheet_names}\n")

# Cargar la primera hoja (o especifica el nombre si lo conoces)
df = pd.read_excel(ruta, sheet_name=xls.sheet_names[0])

print("=== DIMENSIONES ===")
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

print("\n=== PRIMERAS 5 FILAS ===")
print(df.head())

print("\n=== NOMBRES DE COLUMNAS ===")
for i, col in enumerate(df.columns, 1):
    print(f"{i:3d}. {col}")

print("\n=== TIPOS DE DATOS ===")
print(df.dtypes)

print("\n=== VALORES NULOS ===")
print(df.isnull().sum())

print("\n=== DUPLICADOS ===")
print(f"Total: {df.duplicated().sum()}")
