"""
Visualizaciones adicionales de reglas de asociación
Corrección definitiva para pandas 3.x (Copy-on-Write)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path
from mlxtend.preprocessing import TransactionEncoder

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_PROCESSED, FIGURES_DIR

print("Regenerando visualizaciones de asociacion...")

df = pd.read_csv(DATA_PROCESSED / 'df_clustering.csv')
reglas = pd.read_csv(DATA_PROCESSED / 'reglas_asociacion.csv')

# =====================================================
# Recrear df_encoded
# =====================================================
df_trans = pd.DataFrame(index=df.index)
df_trans['GDP'] = pd.cut(df['gdp_per_capita_current_usd'],
                         bins=[0, 2000, 15000, np.inf],
                         labels=['GDP_Bajo', 'GDP_Medio', 'GDP_Alto'])
df_trans['Gini'] = pd.cut(df['gini_index'],
                          bins=[0, 33, 42, 100],
                          labels=['Gini_Bajo', 'Gini_Medio', 'Gini_Alto'])
df_trans['Mortalidad'] = pd.cut(df['under5_mortality_rate'],
                                bins=[0, 15, 50, np.inf],
                                labels=['Mort_Baja', 'Mort_Media', 'Mort_Alta'])
df_trans['Pobreza'] = pd.cut(df['poverty_headcount_3_dollars_pct'],
                             bins=[-1, 2, 20, 100],
                             labels=['Pob_Baja', 'Pob_Media', 'Pob_Alta'])

transacciones = df_trans.astype(str).values.tolist()
te = TransactionEncoder()
te_array = te.fit(transacciones).transform(transacciones)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)

# =====================================================
# HEATMAP DE CO-OCURRENCIA (CORREGIDO DEFINITIVO)
# =====================================================
# Convertir a numpy array puro para evitar read-only
cooc_matrix = df_encoded.T.dot(df_encoded).to_numpy().copy()
np.fill_diagonal(cooc_matrix, 0)

# Reconstruir como DataFrame
cooc = pd.DataFrame(cooc_matrix,
                    index=df_encoded.columns,
                    columns=df_encoded.columns)

# Ordenar por frecuencia
orden = df_encoded.sum().sort_values(ascending=False).index
cooc = cooc.loc[orden, orden]

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(cooc, cmap='YlOrRd', annot=False, ax=ax,
            cbar_kws={'label': 'Co-ocurrencia'})
ax.set_title('Matriz de Co-ocurrencia entre Indicadores',
             fontweight='bold', fontsize=13)
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'asociacion_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] asociacion_heatmap.png")

# =====================================================
# TOP 10 REGLAS POR LIFT
# =====================================================
top10 = reglas.head(10).copy()
top10['regla'] = top10['antecedentes'] + ' -> ' + top10['consequents']
top10 = top10.sort_values('lift')

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(top10['regla'], top10['lift'],
               color='steelblue', edgecolor='black')
ax.set_xlabel('Lift')
ax.set_title('Top 10 Reglas de Asociacion por Lift',
             fontweight='bold', fontsize=13)

for bar, conf in zip(bars, top10['confidence']):
    ax.text(bar.get_width() + 0.05,
            bar.get_y() + bar.get_height()/2,
            f'conf={conf:.2f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'asociacion_top10.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] asociacion_top10.png")

# =====================================================
# GRAFICO DE RED DE REGLAS
# =====================================================
np.random.seed(42)
fig, ax = plt.subplots(figsize=(13, 11))

# Recopilar todos los items de las top 20 reglas
items_unicos = set()
for _, row in reglas.head(20).iterrows():
    items_unicos.update(str(row['antecedentes']).split(', '))
    items_unicos.update(str(row['consequents']).split(', '))

items_unicos = sorted(items_unicos)
pos = {item: (np.random.random(), np.random.random())
       for item in items_unicos}

# Dibujar las reglas (líneas)
for _, row in reglas.head(20).iterrows():
    ants = str(row['antecedentes']).split(', ')
    cons = str(row['consequents']).split(', ')
    for a in ants:
        for c in cons:
            if a in pos and c in pos:
                x_a, y_a = pos[a]
                x_c, y_c = pos[c]
                ax.plot([x_a, x_c], [y_a, y_c],
                        alpha=min(row['lift']/12, 0.7),
                        linewidth=row['confidence']*3,
                        color='steelblue', zorder=1)

# Dibujar nodos
for item, (x, y) in pos.items():
    if 'Mort' in item:
        color = 'red'
    elif 'GDP' in item:
        color = 'green'
    elif 'Pob' in item:
        color = 'orange'
    else:
        color = 'purple'

    ax.scatter(x, y, s=600, c=color, alpha=0.7,
               edgecolors='black', linewidth=2, zorder=5)
    ax.text(x, y, item.replace('_', '\n'),
            ha='center', va='center',
            fontsize=7, fontweight='bold', zorder=6)

# Leyenda manual
from matplotlib.patches import Patch
leyenda = [
    Patch(facecolor='red', edgecolor='black', label='Mortalidad'),
    Patch(facecolor='green', edgecolor='black', label='GDP'),
    Patch(facecolor='orange', edgecolor='black', label='Pobreza'),
    Patch(facecolor='purple', edgecolor='black', label='Gini')
]
ax.legend(handles=leyenda, loc='upper right', fontsize=10)

ax.set_title('Red de Reglas de Asociacion (top 20 por lift)',
             fontweight='bold', fontsize=13)
ax.axis('off')
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'asociacion_red.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] asociacion_red.png")

print("\n[FIN] Visualizaciones regeneradas")
