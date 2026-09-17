# Informe Técnico - Reto 4: Data Mining Aplicado a Pobreza Infantil

**Analista:** jdthg
**Fecha:** 2026-09-17
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
| RandomForest | 0.9309 | 0.9405 | 0.9199 | 0.9301 | 0.9812 |
| SVM | 0.8624 | 0.8487 | 0.8821 | 0.8651 | 0.9487 |
| DecisionTree | 0.8523 | 0.8184 | 0.9054 | 0.8597 | 0.9460 |

**Modelo ganador:** RandomForest

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
| K-means | 0.5370 | 0.8997 | 1605.52 | 2 |
| DBSCAN | 0.5602 | 0.5971 | 304.31 | 3 |
| Jerarquico | 0.5615 | 0.7822 | 1371.60 | 2 |

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
| Pob_Alta, GDP_Bajo | frozenset({'Mort_Alta'}) | 0.0797 | 0.6952 | 6.37 |
| Mort_Alta | frozenset({'Pob_Alta', 'GDP_Bajo'}) | 0.0797 | 0.7300 | 6.37 |
| Mort_Alta | frozenset({'Pob_Alta'}) | 0.0955 | 0.8750 | 5.69 |
| Pob_Alta | frozenset({'Mort_Alta'}) | 0.0955 | 0.6206 | 5.69 |
| GDP_Bajo, Mort_Alta | frozenset({'Pob_Alta'}) | 0.0797 | 0.8639 | 5.62 |

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
