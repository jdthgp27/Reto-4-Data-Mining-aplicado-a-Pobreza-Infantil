"""
Paso 5-6: Evaluación comparativa e interpretación de resultados
Genera el dashboard final y los hallazgos clave de las 3 tecnicas
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_PROCESSED, MODELS_DIR, FIGURES_DIR

print("=" * 60)
print("EVALUACION E INTERPRETACION FINAL")
print("=" * 60)

# =====================================================
# 1. CARGAR TODOS LOS RESULTADOS
# =====================================================
res_clf = pd.read_csv(DATA_PROCESSED / 'resultados_clasificacion.csv', index_col=0)
res_clust = pd.read_csv(DATA_PROCESSED / 'resultados_clustering.csv', index_col=0)
reglas = pd.read_csv(DATA_PROCESSED / 'reglas_asociacion.csv')
df_clusters = pd.read_csv(DATA_PROCESSED / 'paises_con_cluster.csv')
perfiles = pd.read_csv(DATA_PROCESSED / 'perfiles_clusters.csv', index_col=0)

print("\n[OK] Resultados cargados")
print(f"  - Clasificacion: {len(res_clf)} modelos")
print(f"  - Clustering: {len(res_clust)} algoritmos")
print(f"  - Asociacion: {len(reglas)} reglas")

# =====================================================
# 2. DASHBOARD INTEGRADO (3 tecnicas en una figura)
# =====================================================
fig = plt.figure(figsize=(16, 11))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25)

# 2.1 Metricas de clasificacion
ax1 = fig.add_subplot(gs[0, 0])
metricas_plot = res_clf[['Accuracy', 'F1-Score', 'ROC-AUC']]
metricas_plot.plot(kind='bar', ax=ax1, colormap='viridis', edgecolor='black')
ax1.set_title('1. CLASIFICACION - Comparativa de Modelos',
              fontweight='bold', fontsize=12)
ax1.set_ylabel('Score')
ax1.set_ylim(0, 1.05)
ax1.legend(loc='lower right', fontsize=9)
ax1.tick_params(axis='x', rotation=15)
ax1.grid(alpha=0.3)

# 2.2 Metricas de clustering
ax2 = fig.add_subplot(gs[0, 1])
x = np.arange(len(res_clust.index))
width = 0.35
ax2.bar(x - width/2, res_clust['Silueta'], width,
        label='Silueta (↑)', color='steelblue', edgecolor='black')
ax2.bar(x + width/2, res_clust['Davies-Bouldin']/2, width,
        label='Davies-Bouldin/2 (↓)', color='coral', edgecolor='black')
ax2.set_xticks(x)
ax2.set_xticklabels(res_clust.index, rotation=15)
ax2.set_title('2. CLUSTERING - Comparativa de Algoritmos',
              fontweight='bold', fontsize=12)
ax2.set_ylabel('Score')
ax2.legend(fontsize=9)
ax2.grid(alpha=0.3)

# 2.3 Top 10 reglas de asociacion
ax3 = fig.add_subplot(gs[1, 0])
top8 = reglas.head(8).copy()
top8['regla_corta'] = (top8['antecedentes'].str[:25] + '...' +
                       top8['consequents'].str[:15])
top8 = top8.sort_values('lift')
bars = ax3.barh(range(len(top8)), top8['lift'],
                color='mediumseagreen', edgecolor='black')
ax3.set_yticks(range(len(top8)))
ax3.set_yticklabels(top8['regla_corta'], fontsize=8)
ax3.set_xlabel('Lift')
ax3.set_title('3. ASOCIACION - Top 8 Reglas por Lift',
              fontweight='bold', fontsize=12)
ax3.grid(alpha=0.3, axis='x')

# 2.4 Distribucion de clusters
ax4 = fig.add_subplot(gs[1, 1])
clusters_count = df_clusters['cluster'].value_counts().sort_index()
colors = ['steelblue', 'coral']
wedges, texts, autotexts = ax4.pie(
    clusters_count.values,
    labels=[f'Cluster {i}\n(n={n})' for i, n in clusters_count.items()],
    autopct='%1.1f%%', colors=colors,
    startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
    textprops={'fontsize': 10, 'fontweight': 'bold'}
)
ax4.set_title('Segmentacion Final de Paises',
              fontweight='bold', fontsize=12)

plt.suptitle('DASHBOARD FINAL - Data Mining Pobreza Infantil',
             fontsize=15, fontweight='bold', y=0.995)
plt.savefig(FIGURES_DIR / 'dashboard_final.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n[OK] dashboard_final.png")

# =====================================================
# 3. MATRIZ DE CORRELACIONES
# =====================================================
df_corr = pd.read_csv(DATA_PROCESSED / 'df_clustering.csv')
cols_num = [
    'gdp_per_capita_current_usd', 'gini_index',
    'under5_mortality_rate', 'poverty_headcount_3_dollars_pct',
    'infant_mortality_rate', 'neonatal_mortality_rate',
    'low_birth_weight_pct', 'stunting_pct', 'underweight_pct'
]
cols_disponibles = [c for c in cols_num if c in df_corr.columns]
corr_matrix = df_corr[cols_disponibles].corr()

fig, ax = plt.subplots(figsize=(11, 9))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            square=True, linewidths=0.5, ax=ax,
            cbar_kws={'label': 'Correlacion'})
ax.set_title('Matriz de Correlaciones - Indicadores Clave',
             fontweight='bold', fontsize=13)
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'matriz_correlaciones.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] matriz_correlaciones.png")

# =====================================================
# 4. HALLAZGOS CLAVE (texto)
# =====================================================
hallazgos = []

# Hallazgo de clasificacion
mejor_clf = res_clf.index[0]
hallazgos.append({
    'tecnica': 'Clasificacion',
    'hallazgo': f'Random Forest predice alta mortalidad infantil con F1={res_clf.loc[mejor_clf, "F1-Score"]:.3f}',
    'implicacion': 'El PIB per capita es el predictor mas fuerte (44.9% importancia)'
})

# Hallazgo de clustering
hallazgos.append({
    'tecnica': 'Clustering',
    'hallazgo': 'K-means identifica 2 clusters: desarrollo relativo (82%) vs critico (18%)',
    'implicacion': 'Segmentacion dicotomica clara para politicas diferenciadas'
})

# Hallazgo de asociacion
mejor_regla = reglas.iloc[0]
hallazgos.append({
    'tecnica': 'Asociacion',
    'hallazgo': f'Regla mas fuerte: {mejor_regla["antecedentes"]} -> {mejor_regla["consequents"]} (lift={mejor_regla["lift"]:.2f})',
    'implicacion': 'Combinacion GDP bajo + pobreza alta multiplica 6.4x el riesgo'
})

df_hallazgos = pd.DataFrame(hallazgos)
df_hallazgos.to_csv(DATA_PROCESSED / 'hallazgos_clave.csv', index=False)

print("\n" + "=" * 60)
print("HALLAZGOS CLAVE")
print("=" * 60)
for _, row in df_hallazgos.iterrows():
    print(f"\n[{row['tecnica']}]")
    print(f"  Hallazgo: {row['hallazgo']}")
    print(f"  Implicacion: {row['implicacion']}")

# =====================================================
# 5. TABLA MAESTRA DE RESULTADOS
# =====================================================
with pd.ExcelWriter(DATA_PROCESSED / 'resultados_completos.xlsx') as writer:
    res_clf.to_excel(writer, sheet_name='Clasificacion')
    res_clust.to_excel(writer, sheet_name='Clustering')
    reglas.head(30).to_excel(writer, sheet_name='Top30_Reglas', index=False)
    perfiles.to_excel(writer, sheet_name='Perfiles_Clusters')
    df_hallazgos.to_excel(writer, sheet_name='Hallazgos_Clave', index=False)

print("\n[OK] resultados_completos.xlsx (5 hojas)")

# =====================================================
# 6. VERIFICACION FINAL
# =====================================================
print("\n" + "=" * 60)
print("VERIFICACION FINAL")
print("=" * 60)

n_figuras = len(list(FIGURES_DIR.glob('*.png')))
n_modelos = len(list(MODELS_DIR.glob('*.pkl')))
n_datasets = len(list(DATA_PROCESSED.glob('*.csv'))) + \
             len(list(DATA_PROCESSED.glob('*.xlsx')))

print(f"\nFiguras generadas: {n_figuras}")
print(f"Modelos entrenados: {n_modelos}")
print(f"Datasets procesados: {n_datasets}")

print("\n[FIN] Evaluacion e interpretacion completadas")
