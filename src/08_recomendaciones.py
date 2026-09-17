"""
Paso 7: Desarrollo de recomendaciones de negocio
Genera el informe de recomendaciones basado en los hallazgos
"""
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_PROCESSED, MODELS_DIR, FIGURES_DIR, BASE_DIR

print("=" * 60)
print("PASO 7: DESARROLLO DE RECOMENDACIONES")
print("=" * 60)

# =====================================================
# CARGAR RESULTADOS
# =====================================================
res_clf = pd.read_csv(DATA_PROCESSED / 'resultados_clasificacion.csv', index_col=0)
reglas = pd.read_csv(DATA_PROCESSED / 'reglas_asociacion.csv')
df_clusters = pd.read_csv(DATA_PROCESSED / 'paises_con_cluster.csv')
hallazgos = pd.read_csv(DATA_PROCESSED / 'hallazgos_clave.csv')

# =====================================================
# ESTRUCTURA DE RECOMENDACIONES POR CLUSTER
# =====================================================
recomendaciones = []

# ============ RECOMENDACIONES CLUSTER 0 (DESARROLLO RELATIVO) ============
cluster_0 = df_clusters[df_clusters['cluster'] == 0]
recomendaciones.append({
    'id': 'R1',
    'cluster': 0,
    'segmento': 'Paises con desarrollo relativo',
    'n_paises': len(cluster_0),
    'hallazgo': 'Cluster 0: GDP promedio $21.8k, mortalidad 10.8, pobreza 2.8%',
    'accion': 'Programas de mantenimiento y prevencion temprana',
    'objetivo_smart': 'Mantener mortalidad infantil <15 por 1000 nacidos vivos en 2027',
    'recursos': 'Sistema de alerta temprana (presupuesto bajo, 5% del total)',
    'kpi': 'Tasa de mortalidad infantil anual',
    'riesgo': 'Complacencia por bajos indicadores actuales'
})

# ============ RECOMENDACIONES CLUSTER 1 (CRÍTICO) ============
cluster_1 = df_clusters[df_clusters['cluster'] == 1]
recomendaciones.append({
    'id': 'R2',
    'cluster': 1,
    'segmento': 'Paises en situacion critica',
    'n_paises': len(cluster_1),
    'hallazgo': 'Cluster 1: GDP $1.6k, mortalidad 68.2, pobreza 39.5% (lift=6.37)',
    'accion': 'Intervencion integral de emergencia humanitaria',
    'objetivo_smart': 'Reducir mortalidad infantil 30% y pobreza extrema 25% en 3 anos',
    'recursos': 'Fondos multilaterales (UNICEF, BM) + cooperacion internacional',
    'kpi': 'Reduccion de mortalidad <5 anos y pobreza <3 USD',
    'riesgo': 'Inestabilidad politica, conflictos armados, corrupcion'
})

# ============ RECOMENDACIONES POR REGLA DE ASOCIACION ============
recomendaciones.append({
    'id': 'R3',
    'cluster': 'Todos',
    'segmento': 'Priorizar cuando coincidan GDP bajo + pobreza alta',
    'n_paises': 'Segmento transversal',
    'hallazgo': f'Regla: GDP_Bajo + Pob_Alta -> Mort_Alta (lift=6.37, conf=0.70)',
    'accion': 'Sistema de alerta temprana basado en combinacion de indicadores',
    'objetivo_smart': 'Identificar 100% de paises en riesgo alto en 6 meses',
    'recursos': 'Dashboard interactivo + analistas de datos (mediano)',
    'kpi': 'Precision de alertas, tiempo de respuesta',
    'riesgo': 'Datos desactualizados para algunos paises'
})

# ============ RECOMENDACIONES POR CLASIFICACION ============
recomendaciones.append({
    'id': 'R4',
    'cluster': 'Todos',
    'segmento': 'Optimizacion presupuestaria basada en modelo predictivo',
    'n_paises': 'Todos los paises elegibles',
    'hallazgo': f'Random Forest F1={res_clf.iloc[0]["F1-Score"]:.3f}, PIB es 45% de la importancia',
    'accion': 'Priorizar inversiones en desarrollo economico como base de salud infantil',
    'objetivo_smart': 'Aumentar GDP per capita 5% anual en paises criticos',
    'recursos': 'Programas economicos + inversiones en infraestructura',
    'kpi': 'GDP per capita, indice de desarrollo humano',
    'riesgo': 'Crecimiento economico desigual, beneficiando solo elite'
})

# ============ RECOMENDACIONES ADICIONALES ============
recomendaciones.append({
    'id': 'R5',
    'cluster': 'Todos',
    'segmento': 'Monitoreo continuo con modelo predictivo',
    'n_paises': 'Todos',
    'hallazgo': 'Modelo entrenado puede predecir nuevos casos con 93% de F1',
    'accion': 'Implementar pipeline automatizado de prediccion anual',
    'objetivo_smart': 'Actualizar predicciones anualmente con nuevos datos',
    'recursos': 'Infraestructura de datos + equipo tecnico (mediano-alto)',
    'kpi': 'Frecuencia de actualizacion, uso del modelo en decisiones',
    'riesgo': 'Deriva del modelo (concept drift) por cambios socioeconomicos'
})

df_recs = pd.DataFrame(recomendaciones)
df_recs.to_csv(DATA_PROCESSED / 'recomendaciones.csv', index=False)

print(f"\n[OK] {len(df_recs)} recomendaciones generadas")

# =====================================================
# GENERAR INFORME MARKDOWN DE RECOMENDACIONES
# =====================================================
fecha = datetime.now().strftime('%Y-%m-%d')

reporte_md = f"""# Recomendaciones de Negocio - Pobreza Infantil
## Reto 4: Aplicación de Técnicas Avanzadas de Data Mining

**Fecha:** {fecha}
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

"""

for _, h in hallazgos.iterrows():
    reporte_md += f"""### Hallazgo: {h['tecnica']}

**Descubrimiento:** {h['hallazgo']}

**Implicación de negocio:** {h['implicacion']}

"""

reporte_md += """
---

## 3. Recomendaciones por Segmento

"""

for _, r in df_recs.iterrows():
    reporte_md += f"""### [{r['id']}] {r['segmento']}

| Atributo | Valor |
|----------|-------|
| **Cluster objetivo** | {r['cluster']} |
| **Países afectados** | {r['n_paises']} |
| **Hallazgo base** | {r['hallazgo']} |
| **Acción recomendada** | {r['accion']} |
| **Objetivo SMART** | {r['objetivo_smart']} |
| **Recursos necesarios** | {r['recursos']} |
| **KPI de seguimiento** | {r['kpi']} |
| **Riesgo principal** | {r['riesgo']} |

"""

reporte_md += f"""
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
"""

# Guardar informe
reports_final = BASE_DIR / 'reports' / 'final'
reports_final.mkdir(parents=True, exist_ok=True)
with open(reports_final / 'Recomendaciones_Reto4_jdthg.md', 'w', encoding='utf-8') as f:
    f.write(reporte_md)

print(f"[OK] Informe de recomendaciones generado")
print(f"     {reports_final / 'Recomendaciones_Reto4_jdthg.md'}")

# =====================================================
# RESUMEN
# =====================================================
print("\n" + "=" * 60)
print("RESUMEN DE RECOMENDACIONES")
print("=" * 60)
for _, r in df_recs.iterrows():
    print(f"\n[{r['id']}] {r['segmento']}")
    print(f"    Accion: {r['accion']}")
    print(f"    Objetivo: {r['objetivo_smart']}")

print("\n[FIN] Recomendaciones completadas")
