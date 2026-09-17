"""
Paso 3: Preparación de datos
Genera dos datasets:
  - df_clasificacion.csv: para clasificación (mortalidad infantil)
  - df_clustering.csv: para clustering y asociación
"""
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_RAW, DATA_PROCESSED, DATASET_NAME, RANDOM_STATE

# =====================================================
# 1. CARGAR DATOS
# =====================================================
print("Cargando dataset original...")
df = pd.read_excel(DATA_RAW / DATASET_NAME)
print(f"Registros originales: {len(df):,}\n")

# =====================================================
# 2. SELECCIONAR COLUMNAS RELEVANTES
# =====================================================
cols_relevantes = [
    'country_id', 'country_name', 'iso2_code', 'year',
    'gdp_per_capita_current_usd', 'gdp_billions_usd',
    'gini_index', 'poverty_headcount_3_dollars_pct',
    'poverty_headcount_4_dollars_pct', 'poverty_headcount_8_dollars_pct',
    'under5_mortality_rate', 'infant_mortality_rate', 'neonatal_mortality_rate',
    'low_birth_weight_pct', 'stunting_pct', 'underweight_pct', 'wasting_pct',
    'education_spending_pct_gdp', 'govt_expense_pct_gdp',
    'child_poverty_pv_chld_dprv-avg-hs', 'child_poverty_pv_level'
]

cols_existentes = [c for c in cols_relevantes if c in df.columns]
df = df[cols_existentes].copy()
print(f"Columnas seleccionadas: {len(cols_existentes)}\n")

# =====================================================
# 3. FILTRAR POR AÑO >= 2000
# =====================================================
df = df[df['year'] >= 2000].copy()
print(f"Registros tras filtrar año>=2000: {len(df):,}")

# =====================================================
# 4. DATASET PARA CLASIFICACIÓN
# =====================================================
print("\n--- Preparando dataset de CLASIFICACIÓN ---")
df_clf = df.dropna(subset=['under5_mortality_rate', 'gdp_per_capita_current_usd']).copy()
print(f"Registros con variables clave: {len(df_clf):,}")

mediana_mort = df_clf['under5_mortality_rate'].median()
df_clf['high_child_mortality'] = (
    df_clf['under5_mortality_rate'] > mediana_mort
).astype(int)

print(f"Mediana mortalidad <5 años: {mediana_mort:.2f}")
print(f"Distribución variable objetivo:")
print(df_clf['high_child_mortality'].value_counts())
print(f"Balance: {df_clf['high_child_mortality'].mean()*100:.1f}% clase alta")

# =====================================================
# 5. DATASET PARA CLUSTERING Y ASOCIACIÓN
# =====================================================
print("\n--- Preparando dataset de CLUSTERING/ASOCIACIÓN ---")
cols_cluster = [
    'gdp_per_capita_current_usd', 'gini_index',
    'under5_mortality_rate', 'poverty_headcount_3_dollars_pct'
]
df_clust = df.dropna(subset=cols_cluster, thresh=3).copy()

# Imputación compatible con pandas 3.x (sin inplace encadenado)
for c in cols_cluster:
    if df_clust[c].isnull().any():
        df_clust[c] = df_clust[c].fillna(df_clust[c].median())

print(f"Registros para clustering: {len(df_clust):,}")
print(f"Países únicos: {df_clust['country_name'].nunique()}")

# =====================================================
# 6. LIMPIEZA FINAL: OUTLIERS EXTREMOS
# =====================================================
df_clf = df_clf[df_clf['gdp_per_capita_current_usd'] > 0]
df_clust = df_clust[df_clust['gdp_per_capita_current_usd'] > 0]

# =====================================================
# 7. GUARDAR DATASETS
# =====================================================
df_clf.to_csv(DATA_PROCESSED / 'df_clasificacion.csv', index=False)
df_clust.to_csv(DATA_PROCESSED / 'df_clustering.csv', index=False)

print(f"\n[OK] Dataset clasificacion guardado: {len(df_clf):,} filas")
print(f"[OK] Dataset clustering guardado: {len(df_clust):,} filas")
print(f"\nArchivos en: {DATA_PROCESSED}")
