"""
Paso 4.2: Clustering - Segmentación de países por perfil de pobreza
Modelos: K-means, DBSCAN, Clustering Jerárquico
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import sys
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.cluster.hierarchy import dendrogram, linkage

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_PROCESSED, MODELS_DIR, FIGURES_DIR, RANDOM_STATE

print("=" * 60)
print("CLUSTERING - Segmentacion de paises por pobreza infantil")
print("=" * 60)

# =====================================================
# 1. CARGAR DATOS
# =====================================================
df = pd.read_csv(DATA_PROCESSED / 'df_clustering.csv')
print(f"\nDataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")

cols_cluster = [
    'gdp_per_capita_current_usd', 'gini_index',
    'under5_mortality_rate', 'poverty_headcount_3_dollars_pct'
]
X = df[cols_cluster].copy()

# =====================================================
# 2. TRATAMIENTO DE OUTLIERS (percentil 99)
# =====================================================
print(f"\nAntes de tratar outliers:")
print(X.describe().round(2))

for col in X.columns:
    q99 = X[col].quantile(0.99)
    X[col] = X[col].clip(upper=q99)

print(f"\nDespues de recortar a percentil 99:")
print(X.describe().round(2))

# =====================================================
# 3. TRANSFORMACION LOG DE GDP + ESCALADO
# =====================================================
# GDP tiene rango enorme (162 a 134.966), aplicamos log
X['gdp_per_capita_log'] = np.log1p(X['gdp_per_capita_current_usd'])

# Variables finales para clustering
cols_final = ['gdp_per_capita_log', 'gini_index',
              'under5_mortality_rate', 'poverty_headcount_3_dollars_pct']
X_final = X[cols_final].copy()

# Escalado
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_final)
print(f"\nDatos escalados: media~0, std~1")
print(f"Shape final: {X_scaled.shape}")

# =====================================================
# 4. DETERMINAR K OPTIMO (metodo del codo + silueta)
# =====================================================
print("\n--- Buscando K optimo para K-means ---")

inercias = []
siluetas = []
davies = []
K_range = range(2, 9)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    labels = km.fit_predict(X_scaled)
    inercias.append(km.inertia_)
    siluetas.append(silhouette_score(X_scaled, labels))
    davies.append(davies_bouldin_score(X_scaled, labels))
    print(f"  K={k}: inertia={km.inertia_:.1f}, silueta={siluetas[-1]:.4f}, davies={davies[-1]:.4f}")

# K optimo por silueta
k_optimo = K_range[np.argmax(siluetas)]
print(f"\n>>> K optimo por silueta: {k_optimo} (silueta={max(siluetas):.4f})")

# =====================================================
# 5. GRAFICO DEL CODO + SILUETA
# =====================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(K_range, inercias, 'bo-', linewidth=2, markersize=8)
axes[0].axvline(k_optimo, color='red', linestyle='--', alpha=0.7, label=f'K optimo={k_optimo}')
axes[0].set_xlabel('Numero de clusters (K)')
axes[0].set_ylabel('Inercia')
axes[0].set_title('Metodo del Codo', fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(K_range, siluetas, 'go-', linewidth=2, markersize=8)
axes[1].axvline(k_optimo, color='red', linestyle='--', alpha=0.7, label=f'K optimo={k_optimo}')
axes[1].set_xlabel('Numero de clusters (K)')
axes[1].set_ylabel('Indice de Silueta')
axes[1].set_title('Indice de Silueta por K', fontweight='bold')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clustering_k_optimo.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clustering_k_optimo.png")

# =====================================================
# 6. ENTRENAR 3 ALGORITMOS
# =====================================================
print("\n--- Entrenando 3 algoritmos de clustering ---")

# 6.1 K-means
km_final = KMeans(n_clusters=k_optimo, random_state=RANDOM_STATE, n_init=10)
labels_km = km_final.fit_predict(X_scaled)

# 6.2 DBSCAN
dbscan = DBSCAN(eps=0.8, min_samples=10)
labels_db = dbscan.fit_predict(X_scaled)
n_clusters_db = len(set(labels_db)) - (1 if -1 in labels_db else 0)
n_noise_db = list(labels_db).count(-1)

# 6.3 Jerarquico
hc = AgglomerativeClustering(n_clusters=k_optimo, linkage='ward')
labels_hc = hc.fit_predict(X_scaled)

# =====================================================
# 7. METRICAS COMPARATIVAS
# =====================================================
def evaluar(nombre, labels, X_data):
    mask = labels != -1
    if len(set(labels[mask])) < 2:
        return {'Modelo': nombre, 'Silueta': np.nan,
                'Davies-Bouldin': np.nan, 'Calinski-Harabasz': np.nan,
                'N_Clusters': len(set(labels)), 'Ruido': int((~mask).sum())}
    return {
        'Modelo': nombre,
        'Silueta': silhouette_score(X_data[mask], labels[mask]),
        'Davies-Bouldin': davies_bouldin_score(X_data[mask], labels[mask]),
        'Calinski-Harabasz': calinski_harabasz_score(X_data[mask], labels[mask]),
        'N_Clusters': len(set(labels[mask])),
        'Ruido': int((~mask).sum())
    }

resultados = pd.DataFrame([
    evaluar('K-means', labels_km, X_scaled),
    evaluar('DBSCAN', labels_db, X_scaled),
    evaluar('Jerarquico', labels_hc, X_scaled)
]).set_index('Modelo').round(4)

print("\n" + "=" * 60)
print("COMPARATIVA DE ALGORITMOS DE CLUSTERING")
print("=" * 60)
print(resultados.to_string())
resultados.to_csv(DATA_PROCESSED / 'resultados_clustering.csv')

# =====================================================
# 8. VISUALIZACION PCA 2D
# =====================================================
pca = PCA(n_components=2, random_state=RANDOM_STATE)
X_pca = pca.fit_transform(X_scaled)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for ax, (nombre, labels) in zip(axes, [
    ('K-means', labels_km),
    ('DBSCAN', labels_db),
    ('Jerarquico', labels_hc)
]):
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels,
                        cmap='viridis', s=30, alpha=0.6)
    ax.set_title(f'{nombre}', fontweight='bold')
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
    plt.colorbar(scatter, ax=ax, label='Cluster')

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clustering_pca_comparativa.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clustering_pca_comparativa.png")

# =====================================================
# 9. DENDROGRAMA
# =====================================================
fig, ax = plt.subplots(figsize=(14, 6))
linkage_matrix = linkage(X_scaled, method='ward')
dendrogram(linkage_matrix, truncate_mode='lastp', p=30, ax=ax,
           leaf_rotation=90, leaf_font_size=8)
ax.set_title('Dendrograma - Clustering Jerarquico', fontweight='bold')
ax.set_xlabel('Indice de muestra agrupada')
ax.set_ylabel('Distancia')
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clustering_dendrograma.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clustering_dendrograma.png")

# =====================================================
# 10. PERFIL DE CLUSTERS (K-means, que es el elegido)
# =====================================================
df_resultado = df.copy()
df_resultado['cluster'] = labels_km

print("\n--- PERFIL DE CADA CLUSTER (K-means) ---")
perfil = df_resultado.groupby('cluster')[cols_cluster + ['gini_index']].agg(['mean', 'count'])
perfil.columns = ['_'.join(c).strip() for c in perfil.columns]
print(perfil.round(2).to_string())

# Guardar perfil
perfil.to_csv(DATA_PROCESSED / 'perfiles_clusters.csv')
print("\n[OK] perfiles_clusters.csv")

# =====================================================
# 11. BOXPLOTS POR CLUSTER
# =====================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, col in enumerate(cols_cluster):
    sns.boxplot(data=df_resultado, x='cluster', y=col, ax=axes[i], palette='viridis')
    axes[i].set_title(f'{col} por cluster', fontweight='bold')
    axes[i].set_yscale('log') if col == 'gdp_per_capita_current_usd' else None

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clustering_boxplots.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clustering_boxplots.png")

# =====================================================
# 12. GUARDAR MODELO Y RESULTADOS
# =====================================================
with open(MODELS_DIR / 'kmeans_clustering.pkl', 'wb') as f:
    pickle.dump({
        'modelo': km_final,
        'scaler': scaler,
        'columnas': cols_final,
        'k_optimo': k_optimo
    }, f)

df_resultado[['country_name', 'year', 'cluster'] + cols_cluster].to_csv(
    DATA_PROCESSED / 'paises_con_cluster.csv', index=False
)

print(f"\n[OK] kmeans_clustering.pkl guardado")
print(f"[OK] paises_con_cluster.csv guardado ({len(df_resultado)} filas)")

# =====================================================
# 13. RESUMEN FINAL
# =====================================================
print("\n" + "=" * 60)
print("RESUMEN FINAL - CLUSTERING")
print("=" * 60)
print(f"\nAlgoritmo ganador: K-means (K={k_optimo})")
print(f"Silueta: {silhouette_score(X_scaled, labels_km):.4f}")
print(f"Davies-Bouldin: {davies_bouldin_score(X_scaled, labels_km):.4f}")

print(f"\nTamano de cada cluster:")
print(df_resultado['cluster'].value_counts().sort_index().to_string())

print(f"\nTop 5 paises por cluster (mas recientes):")
for c in sorted(df_resultado['cluster'].unique()):
    top = df_resultado[df_resultado['cluster']==c].sort_values('year', ascending=False).head(5)
    print(f"\n  Cluster {c} (n={len(df_resultado[df_resultado['cluster']==c])}):")
    for _, row in top.iterrows():
        print(f"    {row['country_name']} ({row['year']})")

print("\n[FIN] Clustering completado")
