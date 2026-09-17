# Recomendaciones de Negocio - Pobreza Infantil
## Reto 4: Aplicación de Técnicas Avanzadas de Data Mining

**Fecha:** 2026-09-17
**Analista:** jdthg
**Dataset:** UNICEF/World Bank - Pobreza Infantil (14.105 registros, 217 países, 1960-2024)

---

## 1. Resumen Ejecutivo

Este análisis aplicó tres técnicas avanzadas de Data Mining sobre datos de pobreza infantil
combinados con indicadores socioeconómicos de 217 países:

- **Clasificación** (Random Forest): F1=0.93, ROC-AUC=0.98
- **Clustering** (K-means, K=2): Silueta=0.54
- **Asociación** (FP-Growth): 85 reglas, lift máximo=6.37

### Hallazgo Principal

> **La combinación de PIB bajo + pobreza alta multiplica 6.4 veces el riesgo de mortalidad infantil alta.**

Este hallazgo justifica intervenciones focalizadas en los 329 registros país-año clasificados
como "situación crítica" (África subsahariana principalmente).

---

## 2. Los 3 Hallazgos Clave

### Hallazgo: Clasificacion

**Descubrimiento:** Random Forest predice alta mortalidad infantil con F1=0.930

**Implicación de negocio:** El PIB per capita es el predictor mas fuerte (44.9% importancia)

### Hallazgo: Clustering

**Descubrimiento:** K-means identifica 2 clusters: desarrollo relativo (82%) vs critico (18%)

**Implicación de negocio:** Segmentacion dicotomica clara para politicas diferenciadas

### Hallazgo: Asociacion

**Descubrimiento:** Regla mas fuerte: Pob_Alta, GDP_Bajo -> frozenset({'Mort_Alta'}) (lift=6.37)

**Implicación de negocio:** Combinacion GDP bajo + pobreza alta multiplica 6.4x el riesgo


---

## 3. Recomendaciones por Segmento

### [R1] Paises con desarrollo relativo

| Atributo | Valor |
|----------|-------|
| **Cluster objetivo** | 0 |
| **Países afectados** | 1504 |
| **Hallazgo base** | Cluster 0: GDP promedio $21.8k, mortalidad 10.8, pobreza 2.8% |
| **Acción recomendada** | Programas de mantenimiento y prevencion temprana |
| **Objetivo SMART** | Mantener mortalidad infantil <15 por 1000 nacidos vivos en 2027 |
| **Recursos necesarios** | Sistema de alerta temprana (presupuesto bajo, 5% del total) |
| **KPI de seguimiento** | Tasa de mortalidad infantil anual |
| **Riesgo principal** | Complacencia por bajos indicadores actuales |

### [R2] Paises en situacion critica

| Atributo | Valor |
|----------|-------|
| **Cluster objetivo** | 1 |
| **Países afectados** | 329 |
| **Hallazgo base** | Cluster 1: GDP $1.6k, mortalidad 68.2, pobreza 39.5% (lift=6.37) |
| **Acción recomendada** | Intervencion integral de emergencia humanitaria |
| **Objetivo SMART** | Reducir mortalidad infantil 30% y pobreza extrema 25% en 3 anos |
| **Recursos necesarios** | Fondos multilaterales (UNICEF, BM) + cooperacion internacional |
| **KPI de seguimiento** | Reduccion de mortalidad <5 anos y pobreza <3 USD |
| **Riesgo principal** | Inestabilidad politica, conflictos armados, corrupcion |

### [R3] Priorizar cuando coincidan GDP bajo + pobreza alta

| Atributo | Valor |
|----------|-------|
| **Cluster objetivo** | Todos |
| **Países afectados** | Segmento transversal |
| **Hallazgo base** | Regla: GDP_Bajo + Pob_Alta -> Mort_Alta (lift=6.37, conf=0.70) |
| **Acción recomendada** | Sistema de alerta temprana basado en combinacion de indicadores |
| **Objetivo SMART** | Identificar 100% de paises en riesgo alto en 6 meses |
| **Recursos necesarios** | Dashboard interactivo + analistas de datos (mediano) |
| **KPI de seguimiento** | Precision de alertas, tiempo de respuesta |
| **Riesgo principal** | Datos desactualizados para algunos paises |

### [R4] Optimizacion presupuestaria basada en modelo predictivo

| Atributo | Valor |
|----------|-------|
| **Cluster objetivo** | Todos |
| **Países afectados** | Todos los paises elegibles |
| **Hallazgo base** | Random Forest F1=0.930, PIB es 45% de la importancia |
| **Acción recomendada** | Priorizar inversiones en desarrollo economico como base de salud infantil |
| **Objetivo SMART** | Aumentar GDP per capita 5% anual en paises criticos |
| **Recursos necesarios** | Programas economicos + inversiones en infraestructura |
| **KPI de seguimiento** | GDP per capita, indice de desarrollo humano |
| **Riesgo principal** | Crecimiento economico desigual, beneficiando solo elite |

### [R5] Monitoreo continuo con modelo predictivo

| Atributo | Valor |
|----------|-------|
| **Cluster objetivo** | Todos |
| **Países afectados** | Todos |
| **Hallazgo base** | Modelo entrenado puede predecir nuevos casos con 93% de F1 |
| **Acción recomendada** | Implementar pipeline automatizado de prediccion anual |
| **Objetivo SMART** | Actualizar predicciones anualmente con nuevos datos |
| **Recursos necesarios** | Infraestructura de datos + equipo tecnico (mediano-alto) |
| **KPI de seguimiento** | Frecuencia de actualizacion, uso del modelo en decisiones |
| **Riesgo principal** | Deriva del modelo (concept drift) por cambios socioeconomicos |


---

## 4. Cronograma de Implementación

| Fase | Duración | Acciones |
|------|----------|----------|
| **Corto plazo (0-6 meses)** | 6 meses | R3: Sistema de alerta temprana; R5: Pipeline de predicción |
| **Medio plazo (6-18 meses)** | 12 meses | R1: Programas de prevención; R2: Intervención de emergencia |
| **Largo plazo (18-36 meses)** | 18 meses | R4: Inversiones en desarrollo económico |

---

## 5. Indicadores Clave de Seguimiento (KPIs)

| KPI | Valor actual | Objetivo 2027 | Frecuencia |
|-----|--------------|---------------|------------|
| Mortalidad infantil <5 años (cluster 1) | 68.2/1000 | <48/1000 | Anual |
| Pobreza <3 USD (cluster 1) | 39.5% | <30% | Anual |
| GDP per cápita (países críticos) | $1.569 | $1.900 | Anual |
| Precisión del modelo predictivo | F1=0.93 | F1>0.90 | Anual |
| Cobertura del sistema de alerta | 0% | 100% | Semestral |

---

## 6. Riesgos y Consideraciones

1. **Calidad de datos**: Algunos países tienen datos limitados (cobertura <50%)
2. **Deriva del modelo**: Los patrones socioeconómicos cambian; requiere reentrenamiento anual
3. **Sesgo geográfico**: El modelo está dominado por países de renta media; validar en extremos
4. **Contexto político**: Las recomendaciones asumen estabilidad institucional
5. **Recursos limitados**: Priorizar acciones de mayor impacto y menor costo

---

## 7. Próximos Pasos

1. Validar hallazgos con expertos en desarrollo internacional
2. Ampliar análisis con datos sub-nacionales
3. Integrar variables cualitativas (conflictos, gobernanza)
4. Establecer alianzas con UNICEF, Banco Mundial, OMS
5. Crear dashboard interactivo para tomadores de decisión

---

**Archivos relacionados:**
- Código: `src/01_exploracion.py` a `src/08_recomendaciones.py`
- Modelos: `models/mejor_modelo_clasificacion.pkl`, `models/kmeans_clustering.pkl`
- Visualizaciones: `reports/figures/` (15 figuras)
- Datos procesados: `data/processed/` (9 archivos)

**Fin del informe**
