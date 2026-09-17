"""
Paso 4.3: Asociación - Reglas entre indicadores socioeconómicos y pobreza infantil
Algoritmos: Apriori y FP-Growth
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import sys
from pathlib import Path

from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_PROCESSED, MODELS_DIR, FIGURES_DIR, RANDOM_STATE

print("=" * 60)
print("ASOCIACION - Patrones entre indicadores y pobreza infantil")
print("=" * 60)

# =====================================================
# 1. CARGAR DATOS
# =====================================================
df = pd.read_csv(DATA_PROCESSED / 'df_clustering.csv')
print(f"\nDataset cargado: {df.shape[0]} filas")

# =====================================================
# 2. DISCRETIZAR VARIABLES NUMERICAS
# =====================================================
# Creamos categorias interpretables para cada variable clave
df_trans = pd.DataFrame(index=df.index)

# GDP per capita -> 3 categorias
df_trans['GDP'] = pd.cut(df['gdp_per_capita_current_usd'],
                         bins=[0, 2000, 15000, np.inf],
                         labels=['GDP_Bajo', 'GDP_Medio', 'GDP_Alto'])

# Gini -> 3 categorias
df_trans['Gini'] = pd.cut(df['gini_index'],
                          bins=[0, 33, 42, 100],
                          labels=['Gini_Bajo', 'Gini_Medio', 'Gini_Alto'])

# Mortalidad <5 -> 3 categorias (target conceptual)
df_trans['Mortalidad'] = pd.cut(df['under5_mortality_rate'],
                                bins=[0, 15, 50, np.inf],
                                labels=['Mort_Baja', 'Mort_Media', 'Mort_Alta'])

# Pobreza 3$ -> 3 categorias
df_trans['Pobreza'] = pd.cut(df['poverty_headcount_3_dollars_pct'],
                             bins=[-1, 2, 20, 100],
                             labels=['Pob_Baja', 'Pob_Media', 'Pob_Alta'])

print("\nDistribucion de categorias:")
for c in df_trans.columns:
    print(f"\n{c}:")
    print(df_trans[c].value_counts().to_string())

# =====================================================
# 3. TRANSFORMAR A FORMATO TRANSACCIONAL
# =====================================================
# Cada fila = una "transaccion" con las categorias a las que pertenece
transacciones = df_trans.astype(str).values.tolist()

te = TransactionEncoder()
te_array = te.fit(transacciones).transform(transacciones)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)

print(f"\nDataset transaccional: {df_encoded.shape}")
print(f"Items unicos: {df_encoded.shape[1]}")

# =====================================================
# 4. APRIORI
# =====================================================
print("\n--- Ejecutando APRIORI ---")
itemsets_ap = apriori(df_encoded, min_support=0.05, use_colnames=True, max_len=4)
itemsets_ap['length'] = itemsets_ap['itemsets'].apply(len)

print(f"Itemsets frecuentes: {len(itemsets_ap)}")
print(f"\nTop 10 itemsets mas frecuentes:")
print(itemsets_ap.sort_values('support', ascending=False).head(10).to_string())

# =====================================================
# 5. FP-GROWTH (mas eficiente)
# =====================================================
print("\n--- Ejecutando FP-GROWTH ---")
itemsets_fp = fpgrowth(df_encoded, min_support=0.05, use_colnames=True, max_len=4)
itemsets_fp['length'] = itemsets_fp['itemsets'].apply(len)

print(f"Itemsets frecuentes: {len(itemsets_fp)}")
print(f"Coinciden con Apriori: {len(itemsets_ap)} itemsets")

# =====================================================
# 6. GENERAR REGLAS DE ASOCIACION
# =====================================================
print("\n--- Generando reglas de asociacion ---")

reglas = association_rules(itemsets_fp, metric="confidence",
                           min_threshold=0.6, num_itemsets=len(itemsets_fp))

# Filtrar por lift > 1 (asociacion positiva real)
reglas = reglas[reglas['lift'] > 1.1].copy()
reglas = reglas.sort_values('lift', ascending=False)

print(f"Total reglas generadas: {len(reglas)}")

# Formatear para legibilidad
reglas['antecedentes'] = reglas['antecedents'].apply(lambda x: ', '.join(list(x)))
reglas['consecuentes'] = reglas['consequents'].apply(lambda x: ', '.join(list(x)))

print("\n--- TOP 15 REGLAS POR LIFT ---")
top = reglas[['antecedentes', 'consecuentes', 'support', 'confidence', 'lift']].head(15)
print(top.round(4).to_string(index=False))

reglas.to_csv(DATA_PROCESSED / 'reglas_asociacion.csv', index=False)

# =====================================================
# 7. REGLAS ESPECIFICAS DE MORTALIDAD ALTA
# =====================================================
print("\n--- REGLAS QUE PREDICEN MORTALIDAD ALTA ---")
reglas_mort = reglas[reglas['consecuentes'].str.contains('Mort_Alta')].copy()
print(f"Total: {len(reglas_mort)} reglas")
print(reglas_mort[['antecedentes', 'support', 'confidence', 'lift']].head(10).round(4).to_string(index=False))

# =====================================================
# 8. VISUALIZACION 1: SCATTER SUPPORT vs CONFIDENCE
# =====================================================
fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(reglas['support'], reglas['confidence'],
                    c=reglas['lift'], cmap='viridis',
                    s=reglas['lift']*30, alpha=0.6, edgecolors='black')
plt.colorbar(scatter, label='Lift')
ax.set_xlabel('Soporte (frecuencia)')
ax.set_ylabel('Confianza')
ax.set_title('Reglas de Asociacion: Soporte vs Confianza vs Lift',
             fontweight='bold', fontsize=13)
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'asociacion_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n[OK] asociacion_scatter.png")

# =====================================================
# 9. VISUALIZACION 2: HEATMAP DE CO-OCURRENCIA
# =====================================================
cooc = df_encoded.T.dot(df_encoded)
np.fill_diagonal(cooc.values, 0)

# Ordenar por frecuencia
orden = df_encoded.sum().sort_values(ascending=False).index
cooc = cooc.loc[orden, orden]

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(cooc, cmap='YlOrRd', annot=False, ax=ax, cbar_kws={'label': 'Co-ocurrencia'})
ax.set_title('Matriz de Co-ocurrencia entre Indicadores', fontweight='bold', fontsize=13)
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'asociacion_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] asociacion_heatmap.png")

# =====================================================
# 10. VISUALIZACION 3: TOP 10 REGLAS
# =====================================================
top10 = reglas.head(10).copy()
top10['regla'] = top10['antecedentes'] + ' -> ' + top10['consecuentes']
top10 = top10.sort_values('lift')

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(top10['regla'], top10['lift'], color='steelblue', edgecolor='black')
ax.set_xlabel('Lift')
ax.set_title('Top 10 Reglas de Asociacion por Lift', fontweight='bold', fontsize=13)
for bar, conf in zip(bars, top10['confidence']):
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
            f'conf={conf:.2f}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'asociacion_top10.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] asociacion_top10.png")

# =====================================================
# 11. GUARDAR
# =====================================================
with open(MODELS_DIR / 'reglas_asociacion.pkl', 'wb') as f:
    pickle.dump({
        'itemsets': itemsets_fp,
        'reglas': reglas,
        'columnas_categoricas': list(df_trans.columns)
    }, f)
print("\n[OK] reglas_asociacion.pkl guardado")

# =====================================================
# 12. RESUMEN
# =====================================================
print("\n" + "=" * 60)
print("RESUMEN FINAL - ASOCIACION")
print("=" * 60)
print(f"\nItemsets frecuentes: {len(itemsets_fp)}")
print(f"Reglas totales: {len(reglas)}")
print(f"Reglas con Mort_Alta como consecuente: {len(reglas_mort)}")
print(f"\nLift maximo: {reglas['lift'].max():.3f}")
print(f"Confianza media: {reglas['confidence'].mean():.3f}")

print("\n[FIN] Asociacion completada")
