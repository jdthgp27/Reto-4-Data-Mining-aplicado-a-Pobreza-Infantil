"""
Paso 4.1: Clasificación - Predicción de alta mortalidad infantil
VERSIÓN CORREGIDA: sin data leakage
Modelos: Árbol de Decisión, Random Forest, SVM
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import sys
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_PROCESSED, MODELS_DIR, FIGURES_DIR, RANDOM_STATE, TEST_SIZE

print("=" * 60)
print("CLASIFICACION - Prediccion de alta mortalidad infantil")
print("VERSION SIN DATA LEAKAGE")
print("=" * 60)

df = pd.read_csv(DATA_PROCESSED / 'df_clasificacion.csv')
print(f"\nDataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")

# =====================================================
# 2. FEATURES SIN FUGA DE INFORMACION
# =====================================================
# Excluimos TODAS las variables de mortalidad para evitar leakage
excluir = [
    'country_id', 'country_name', 'iso2_code', 'year',
    # Target
    'high_child_mortality',
    # LEAKAGE: mortalidad (muy correlacionada con la target)
    'under5_mortality_rate', 'infant_mortality_rate', 'neonatal_mortality_rate',
    # Columnas casi vacías
    'child_poverty_pv_chld_dprv-avg-hs', 'child_poverty_pv_level'
]

features = [c for c in df.columns if c not in excluir]
target = 'high_child_mortality'

print(f"\nFeatures utilizadas ({len(features)}):")
for f in features:
    print(f"  - {f}")

X = df[features].copy()
y = df[target].copy()
X = X.fillna(X.median(numeric_only=True))

print(f"\nX: {X.shape} | y: {y.shape}")
print(f"Balance target: {y.value_counts().to_dict()}")

# =====================================================
# 3. TRAIN/TEST SPLIT
# =====================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)
print(f"\nTrain: {len(X_train)} | Test: {len(X_test)}")

# =====================================================
# 4. ESCALADO
# =====================================================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =====================================================
# 5. ENTRENAR MODELOS
# =====================================================
modelos = {
    'DecisionTree': {
        'model': DecisionTreeClassifier(max_depth=5, random_state=RANDOM_STATE),
        'X_train': X_train, 'X_test': X_test
    },
    'RandomForest': {
        'model': RandomForestClassifier(n_estimators=100, max_depth=10,
                                        random_state=RANDOM_STATE, n_jobs=-1),
        'X_train': X_train, 'X_test': X_test
    },
    'SVM': {
        'model': SVC(kernel='rbf', C=1.0, probability=True, random_state=RANDOM_STATE),
        'X_train': X_train_scaled, 'X_test': X_test_scaled
    }
}

resultados = []
for nombre, cfg in modelos.items():
    print(f"\n--- Entrenando {nombre} ---")
    modelo = cfg['model']
    modelo.fit(cfg['X_train'], y_train)
    
    y_pred = modelo.predict(cfg['X_test'])
    y_proba = modelo.predict_proba(cfg['X_test'])[:, 1]
    
    metricas = {
        'Modelo': nombre,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1-Score': f1_score(y_test, y_pred),
        'ROC-AUC': roc_auc_score(y_test, y_proba)
    }
    resultados.append(metricas)
    
    print(f"  Accuracy:  {metricas['Accuracy']:.4f}")
    print(f"  Precision: {metricas['Precision']:.4f}")
    print(f"  Recall:    {metricas['Recall']:.4f}")
    print(f"  F1-Score:  {metricas['F1-Score']:.4f}")
    print(f"  ROC-AUC:   {metricas['ROC-AUC']:.4f}")

# =====================================================
# 6. TABLA COMPARATIVA
# =====================================================
df_resultados = pd.DataFrame(resultados).set_index('Modelo')
df_resultados = df_resultados.round(4).sort_values('F1-Score', ascending=False)

print("\n" + "=" * 60)
print("TABLA COMPARATIVA DE MODELOS")
print("=" * 60)
print(df_resultados.to_string())
df_resultados.to_csv(DATA_PROCESSED / 'resultados_clasificacion.csv')

# =====================================================
# 7. MEJOR MODELO
# =====================================================
mejor_nombre = df_resultados.index[0]
mejor_modelo = modelos[mejor_nombre]['model']
print(f"\n>>> Mejor modelo: {mejor_nombre} (F1={df_resultados.loc[mejor_nombre, 'F1-Score']:.4f})")

with open(MODELS_DIR / 'mejor_modelo_clasificacion.pkl', 'wb') as f:
    pickle.dump({
        'modelo': mejor_modelo,
        'scaler': scaler if mejor_nombre == 'SVM' else None,
        'features': features,
        'nombre': mejor_nombre
    }, f)
print(f"[OK] Modelo guardado")

# =====================================================
# 8. VISUALIZACIONES
# =====================================================
sns.set_style('whitegrid')

# 8.1 Comparativa
fig, ax = plt.subplots(figsize=(10, 6))
df_resultados.plot(kind='bar', ax=ax, colormap='viridis')
ax.set_title('Comparativa de Modelos de Clasificación (sin leakage)', fontsize=14, fontweight='bold')
ax.set_ylabel('Score')
ax.set_ylim(0, 1.05)
ax.legend(loc='lower right')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clasificacion_comparativa.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clasificacion_comparativa.png")

# 8.2 Matriz de confusion
cfg_mejor = modelos[mejor_nombre]
y_pred_mejor = cfg_mejor['model'].predict(cfg_mejor['X_test'])
cm = confusion_matrix(y_test, y_pred_mejor)

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Baja', 'Alta'], yticklabels=['Baja', 'Alta'], ax=ax)
ax.set_title(f'Matriz de Confusion - {mejor_nombre}', fontsize=14, fontweight='bold')
ax.set_xlabel('Prediccion')
ax.set_ylabel('Real')
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clasificacion_matriz_confusion.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clasificacion_matriz_confusion.png")

# 8.3 ROC
fig, ax = plt.subplots(figsize=(8, 7))
for nombre, cfg in modelos.items():
    y_proba = cfg['model'].predict_proba(cfg['X_test'])[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)
    ax.plot(fpr, tpr, label=f'{nombre} (AUC={auc:.3f})', linewidth=2)

ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
ax.set_xlabel('Tasa de Falsos Positivos')
ax.set_ylabel('Tasa de Verdaderos Positivos')
ax.set_title('Curvas ROC - Comparativa de Modelos', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clasificacion_roc.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clasificacion_roc.png")

# 8.4 Arbol
fig, ax = plt.subplots(figsize=(22, 10))
plot_tree(
    modelos['DecisionTree']['model'],
    feature_names=features,
    class_names=['Baja', 'Alta'],
    filled=True, rounded=True, fontsize=9, ax=ax, max_depth=3
)
ax.set_title('Arbol de Decision (primeros 3 niveles)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clasificacion_arbol.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clasificacion_arbol.png")

# 8.5 Importancia features
rf = modelos['RandomForest']['model']
importancias = pd.DataFrame({
    'feature': features,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=importancias, x='importance', y='feature',
            hue='feature', palette='viridis', legend=False, ax=ax)
ax.set_title('Top 10 Features mas importantes (Random Forest)', fontsize=14, fontweight='bold')
ax.set_xlabel('Importancia')
plt.tight_layout()
plt.savefig(FIGURES_DIR / 'clasificacion_importancia.png', dpi=150, bbox_inches='tight')
plt.close()
print("[OK] clasificacion_importancia.png")

# =====================================================
# 9. REPORTE
# =====================================================
print("\n" + "=" * 60)
print("REPORTE FINAL - CLASIFICACION (sin data leakage)")
print("=" * 60)
print(f"\nMejor modelo: {mejor_nombre}")
print(f"\n{classification_report(y_test, y_pred_mejor, target_names=['Baja', 'Alta'])}")

print(f"\nTop 5 features mas importantes (Random Forest):")
for _, row in importancias.head(5).iterrows():
    print(f"  {row['feature']}: {row['importance']:.4f}")

print("\n[FIN] Clasificacion corregida completada")
