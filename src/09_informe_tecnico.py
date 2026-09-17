"""
Genera el informe tecnico completo en Markdown
"""
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_PROCESSED, MODELS_DIR, FIGURES_DIR, BASE_DIR

fecha = datetime.now().strftime('%Y-%m-%d')

# Cargar resultados
res_clf = pd.read_csv(DATA_PROCESSED / 'resultados_clasificacion.csv', index_col=0)
res_clust = pd.read_csv(DATA_PROCESSED / 'resultados_clustering.csv', index_col=0)
reglas = pd.read_csv(DATA_PROCESSED / 'reglas_asociacion.csv')
perfiles = pd.read_csv(DATA_PROCESSED / 'perfiles_clusters.csv', index_col=0)

informe = f"""# Informe Técnico - Reto 4: Data Mining Aplicado a Pobreza Infantil

**Analista:** jdthg
**Fecha:** {fecha}
**Módulo:** BI y Big Data - Nivel 5
**Reto:** Aplicación de Técnicas Avanzadas de Data Mining

---

## 1. Contexto y Objetivo

### Contexto Narrativo
El viajero llega al Santuario de los Secretos Ocultos, donde debe descifrar patrones
y asociaciones en un vasto conjunto de datos sobre pobreza infantil.

### Objetivo del Análisis
Aplicar técnicas avanzadas de Data Mining (clasificación, clustering y asociación)
para extraer insights que informen políticas de reducción de pobreza infantil.

---

## 2. Selección del Dataset

### Fuente
**Repositorio:** `world-bank-unicef-data` (GitHub - danribes)
**Archivo:** `world_bank_gdp_data_with_poverty.xlsx`
**Origen:** Banco Mundial + UNICEF

### Características
- **14.105 registros** (país × año)
- **217 países**
- **64 columnas**
- **Periodo:** 1960-2024
- **Variables:** económicas, fiscales, pobreza, mortalidad infantil, nutrición, desigualdad

### Justificación de la Elección
1. **Volumen suficiente** para algoritmos avanzados
2. **Variables mixtas** (numéricas + categóricas)
3. **Relevancia de negocio** directa: pobreza infantil
4. **Fuentes oficiales** con documentación clara
5. **Cobertura temporal** amplia (64 años)

### Preparación
- Filtrado a partir del año 2000 (mayor calidad de datos)
- Selección de 21 columnas relevantes
- Dos datasets derivados: clasificación (4.577 filas) y clustering (1.833 filas)

---

## 3. Técnicas Aplicadas

### 3.1 CLASIFICACIÓN

**Objetivo:** Predecir si un país tiene alta mortalidad infantil (>mediana 19.84)

**Variables objetivo:** `high_child_mortality` (binaria, balance 50/50)

**Modelos evaluados:**

| Modelo | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|--------|----------|-----------|--------|----------|---------|
"""

for modelo, row in res_clf.iterrows():
    informe += f"| {modelo} | {row['Accuracy']:.4f} | {row['Precision']:.4f} | {row['Recall']:.4f} | {row['F1-Score']:.4f} | {row['ROC-AUC']:.4f} |\n"

informe += f"""
**Modelo ganador:** {res_clf.index[0]}

**Top 5 features más importantes:**
1. gdp_per_capita_current_usd (44.9%)
2. low_birth_weight_pct (10.6%)
3. poverty_headcount_8_dollars_pct (9.6%)
4. poverty_headcount_4_dollars_pct (7.2%)
5. gdp_billions_usd (6.9%)

**Visualizaciones:**
- `clasificacion_comparativa.png`
- `clasificacion_matriz_confusion.png`
- `clasificacion_roc.png`
- `clasificacion_arbol.png`
- `clasificacion_importancia.png`

---

### 3.2 CLUSTERING

**Objetivo:** Segmentar países por perfil de pobreza

**Variables:** GDP, Gini, mortalidad <5, pobreza <3 USD

**Algoritmos evaluados:**

| Algoritmo | Silueta | Davies-Bouldin | Calinski-Harabasz | Clusters |
|-----------|---------|----------------|-------------------|----------|
"""

for alg, row in res_clust.iterrows():
    informe += f"| {alg} | {row['Silueta']:.4f} | {row['Davies-Bouldin']:.4f} | {row['Calinski-Harabasz']:.2f} | {int(row['N_Clusters'])} |\n"

informe += """
**Algoritmo ganador:** K-means con K=2

**Perfiles de clusters:**

| Cluster | Países | GDP | Gini | Mortalidad | Pobreza |
|---------|--------|-----|------|------------|---------|
| 0 | 1.504 | $21.820 | 35.1 | 10.8 | 2.8% |
| 1 | 329 | $1.569 | 43.2 | 68.2 | 39.5% |

**Visualizaciones:**
- `clustering_k_optimo.png`
- `clustering_pca_comparativa.png`
- `clustering_dendrograma.png`
- `clustering_boxplots.png`

---

### 3.3 ASOCIACIÓN

**Objetivo:** Descubrir reglas entre indicadores

**Algoritmos:** Apriori y FP-Growth (mismo resultado: 75 itemsets)

**Parámetros:** soporte ≥ 5%, confianza ≥ 60%, lift > 1.1

**Total reglas:** 85

**Top 5 reglas por lift:**

| Antecedentes | Consecuente | Soporte | Confianza | Lift |
|--------------|-------------|---------|-----------|------|
"""

for _, r in reglas.head(5).iterrows():
    informe += f"| {r['antecedentes']} | {r['consequents']} | {r['support']:.4f} | {r['confidence']:.4f} | {r['lift']:.2f} |\n"

informe += """
**Regla estrella:** `GDP_Bajo + Pob_Alta → Mort_Alta` con lift=6.37

**Visualizaciones:**
- `asociacion_scatter.png`
- `asociacion_heatmap.png`
- `asociacion_top10.png`
- `asociacion_red.png`

---

## 4. Evaluación Comparativa de Modelos

**Criterios de selección:**

| Criterio | Clasificación | Clustering | Asociación |
|----------|---------------|------------|------------|
| **Métrica principal** | F1-Score | Silueta | Lift |
| **Modelo elegido** | Random Forest | K-means (K=2) | FP-Growth |
| **Valor obtenido** | 0.9301 | 0.5370 | 6.37 |
| **Interpretabilidad** | Media (importancia features) | Alta (perfiles claros) | Alta (reglas legibles) |
| **Aplicabilidad** | Alta | Alta | Muy alta |

---

## 5. Interpretación de Resultados

### Insight #1: El PIB es el predictor dominante
El GDP per cápita explica el 44.9% de la capacidad predictiva del modelo.
**Implicación:** Las intervenciones económicas tienen el mayor potencial de impacto.

### Insight #2: Existen dos mundos separados
Los 217 países se dividen claramente en:
- **82%** con desarrollo relativo (mortalidad <11)
- **18%** en situación crítica (mortalidad >68)

**Implicación:** Políticas diferenciadas por segmento.

### Insight #3: La trampa de la pobreza es real
La regla `GDP_Bajo + Pob_Alta → Mort_Alta` con lift 6.37 demuestra
que los factores se refuerzan mutuamente.

**Implicación:** Se requieren intervenciones multidimensionales.

---

## 6. Limitaciones del Análisis

1. **Datos faltantes**: Algunas variables clave tienen <20% de cobertura
2. **Sesgo temporal**: 2024 tiene datos incompletos
3. **Correlación ≠ causalidad**: Los hallazgos son asociativos
4. **Variables omitidas**: No se incluyen factores políticos, culturales o geográficos
5. **Deriva del modelo**: Requiere reentrenamiento anual

---

## 7. Conclusiones

El análisis demuestra que las **técnicas avanzadas de Data Mining** permiten:

1. **Predecir** con alta precisión (F1=0.93) qué países tienen riesgo de mortalidad infantil alta
2. **Segmentar** países en grupos homogéneos para políticas diferenciadas
3. **Descubrir** reglas de asociación que revelan la interacción entre factores
4. **Priorizar** recursos basándose en datos objetivos

El hallazgo más relevante para el negocio es que **la combinación de pobreza extrema y bajo desarrollo económico eleva 6.4x el riesgo de mortalidad infantil**, lo cual justifica un enfoque integrado de intervenciones.

---

## 8. Anexos

### Código fuente
- `src/01_exploracion.py` - Exploración inicial
- `src/02_diagnostico.py` - Diagnóstico de calidad
- `src/03_preparacion.py` - Limpieza y preparación
- `src/04_clasificacion.py` - Clasificación
- `src/05_clustering.py` - Clustering
- `src/06_asociacion.py` - Asociación
- `src/06b_visualizaciones_asociacion.py` - Visualizaciones adicionales
- `src/07_evaluacion_interpretacion.py` - Evaluación
- `src/08_recomendaciones.py` - Recomendaciones

### Modelos entrenados
- `models/mejor_modelo_clasificacion.pkl`
- `models/kmeans_clustering.pkl`
- `models/reglas_asociacion.pkl`

### Datos procesados
- `data/processed/df_clasificacion.csv`
- `data/processed/df_clustering.csv`
- `data/processed/paises_con_cluster.csv`
- `data/processed/perfiles_clusters.csv`
- `data/processed/reglas_asociacion.csv`
- `data/processed/resultados_completos.xlsx`

### Figuras (15)
Todas en `reports/figures/`

---

**Fin del informe técnico**
"""

# Guardar
reports_final = BASE_DIR / 'reports' / 'final'
reports_final.mkdir(parents=True, exist_ok=True)
with open(reports_final / 'Informe_Tecnico_Reto4_jdthg.md', 'w', encoding='utf-8') as f:
    f.write(informe)

print(f"[OK] Informe tecnico generado: {reports_final / 'Informe_Tecnico_Reto4_jdthg.md'}")
