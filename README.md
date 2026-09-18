# 🌍 Reto 4 — Data Mining aplicado a la Pobreza Infantil

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![pandas](https://img.shields.io/badge/pandas-3.0-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13-4C72B0?style=for-the-badge)](https://seaborn.pydata.org/)
[![MLxtend](https://img.shields.io/badge/MLxtend-FP--Growth-2C3E50?style=for-the-badge)](http://rasbt.github.io/mlxtend/)
[![Imbalanced-learn](https://img.shields.io/badge/imbalanced--learn-0.12-FF6F00?style=for-the-badge)](https://imbalanced-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completado-success?style=for-the-badge)]()

> **Análisis avanzado de pobreza infantil en 217 países combinando clasificación, clustering y reglas de asociación para generar recomendaciones de política pública basadas en datos.**

---

## 📖 Descripción

Este proyecto aplica **técnicas avanzadas de Data Mining** sobre un dataset combinado del **Banco Mundial y UNICEF** (14.105 registros, 217 países, 1960-2024) para:

1. **Predecir** qué países tienen alta mortalidad infantil
2. **Segmentar** países por perfil socioeconómico
3. **Descubrir** reglas de asociación entre indicadores
4. **Generar** recomendaciones accionables para políticas públicas

Proyecto desarrollado como parte del módulo **BI y Big Data — Nivel 5** (Odisea Data).

---

## 🎯 Resultados principales

| Técnica | Algoritmo | Métrica | Valor |
|---|---|---|---|
| 🎯 **Clasificación** | Random Forest | F1-Score | **0,9301** |
| 🔵 **Clustering** | K-means (K=2) | Silueta | **0,5370** |
| 🔗 **Asociación** | FP-Growth | Lift máximo | **6,37** |

### 🔑 Los 3 hallazgos clave

1. **El PIB per cápita es el predictor #1** (44,9% de importancia) de la mortalidad infantil alta.
2. **Dos clusters claramente separados**: 82% desarrollo relativo vs 18% situación crítica.
3. **La trampa de la pobreza es cuantificable**: PIB bajo + Pobreza alta → Mortalidad alta (lift = 6,37).

---

## 📊 Dataset

| Atributo | Valor |
|---|---|
| **Fuente** | [World Bank Open Data](https://data.worldbank.org/) + [UNICEF Data](https://data.unicef.org/) |
| **Archivo** | `world_bank_gdp_data_with_poverty.xlsx` |
| **Registros** | 14.105 (país × año) |
| **Países** | 217 |
| **Columnas** | 64 (económicas, fiscales, pobreza, mortalidad, nutrición) |
| **Periodo** | 1960–2024 |

---

## 🔬 Metodología

### 1️⃣ Clasificación

Predicción binaria de `high_child_mortality` usando:

- **Árbol de Decisión** (interpretabilidad)
- **Random Forest** 🥇 (ganador: F1 = 0,93)
- **SVM** (kernel RBF)

**Features clave**: PIB per cápita, bajo peso al nacer, pobreza extrema.

### 2️⃣ Clustering

Segmentación con **K-means**, **DBSCAN** y **clustering jerárquico**.

- **K óptimo**: 2 clusters (método del codo + silueta)

### 3️⃣ Asociación

Reglas con **Apriori** y **FP-Growth** (soporte ≥ 5%, confianza ≥ 60%, lift > 1,1).

- **Resultado**: 85 reglas, siendo la más fuerte `GDP_Bajo + Pob_Alta → Mort_Alta`

---

## 📁 Estructura del proyecto

```
reto4_pobreza_infantil/
│
├── data/
│   ├── raw/                              # Dataset original
│   │   └── world_bank_gdp_data_with_poverty.xlsx
│   └── processed/                        # Datos limpios y resultados
│       ├── df_clasificacion.csv
│       ├── df_clustering.csv
│       ├── hallazgos_clave.csv
│       ├── paises_con_cluster.csv
│       ├── perfiles_clusters.csv
│       ├── recomendaciones.csv
│       ├── reglas_asociacion.csv
│       ├── resultados_clasificacion.csv
│       ├── resultados_clustering.csv
│       └── resultados_completos.xlsx
│
├── models/                               # Modelos entrenados (.pkl)
│   ├── mejor_modelo_clasificacion.pkl
│   └── kmeans_clustering.pkl
│
├── reports/
│   ├── figures/                          # 18 visualizaciones PNG
│   └── final/                            # Entregables finales
│       ├── Informe_Tecnico_Reto4_jdthg.md / .html / .pdf
│       ├── Recomendaciones_Reto4_jdthg.md / .html / .pdf
│       ├── Presentacion-Reto-4-Data-Mining-aplicado-a-Pobreza-Infantil.pptx
│       └── Reto4_DataMining_PobrezaInfantil_jdthg.tar.gz
│
├── src/                                  # Pipeline completo en Python
│   ├── 01_exploracion.py
│   ├── 02_diagnostico.py
│   ├── 03_preparacion.py
│   ├── 04_clasificacion.py
│   ├── 05_clustering.py
│   ├── 06_asociacion.py
│   ├── 06b_visualizaciones_asociacion.py
│   ├── 07_evaluacion_interpretacion.py
│   ├── 08_recomendaciones.py
│   ├── 09_informe_tecnico.py
│   ├── 12_mapa_mundial.py
│   ├── 13_grafico_cobertura.py
│   ├── 10_generar_html.sh
│   ├── 10_generar_informes.sh
│   ├── 10_generar_pdfs.sh
│   ├── 11_empaquetar.sh
│   └── config.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🚀 Instalación y uso

### Requisitos previos

- **Python 3.11+**
- **pip**
- **Git**
- **Pandoc** y **wkhtmltopdf** (solo si quieres regenerar los PDF)

### Instalación

```bash
git clone https://github.com/jdthgp27/Reto-4-Data-Mining-aplicado-a-Pobreza-Infantil.git
cd Reto-4-Data-Mining-aplicado-a-Pobreza-Infantil

python -m venv .venv
source .venv/Scripts/activate    # Windows (Git Bash)
# source .venv/bin/activate      # macOS / Linux

pip install -r requirements.txt
```

### Ejecución del pipeline completo

```bash
python src/01_exploracion.py
python src/02_diagnostico.py
python src/03_preparacion.py
python src/04_clasificacion.py
python src/05_clustering.py
python src/06_asociacion.py
python src/06b_visualizaciones_asociacion.py
python src/07_evaluacion_interpretacion.py
python src/08_recomendaciones.py
python src/09_informe_tecnico.py
python src/12_mapa_mundial.py
python src/13_grafico_cobertura.py
```

### Generar los informes finales (HTML/PDF)

```bash
bash src/10_generar_html.sh
bash src/10_generar_pdfs.sh
bash src/11_empaquetar.sh
```

---

## 📸 Visualizaciones destacadas

### Dashboard final

![Dashboard final](reports/figures/dashboard_final.png)

### Matriz de correlaciones

![Matriz de correlaciones](reports/figures/matriz_correlaciones.png)

### Importancia de features (Random Forest)

![Importancia de features](reports/figures/clasificacion_importancia.png)

### Segmentación de países (PCA)

![Segmentación de países](reports/figures/clustering_pca_comparativa.png)

### Mapa mundial de pobreza infantil

![Mapa mundial de pobreza infantil](reports/figures/mapa_mundial_pobreza.png)

### Reglas de asociación

![Asociación top 10](reports/figures/asociacion_top10.png)

![Red de asociación](reports/figures/asociacion_red.png)

### Matriz de confusión

![Matriz de confusión](reports/figures/clasificacion_matriz_confusion.png)

### Curva ROC

![Curva ROC](reports/figures/clasificacion_roc.png)

> **15+ visualizaciones completas** en `reports/figures/`

---

## 💡 Recomendaciones de negocio

| # | Recomendación | Aplicación |
|---|---|---|
| **R1** | **Países con desarrollo relativo** | Programas de prevención temprana |
| **R2** | **Países en situación crítica** | Intervención humanitaria integral |
| **R3** | **Sistema de alerta temprana** | Basado en PIB bajo + pobreza alta |
| **R4** | **Optimización presupuestaria** | Priorizar desarrollo económico |
| **R5** | **Monitoreo continuo** | Pipeline predictivo anual |

📄 Detalles completos en [Recomendaciones_Reto4_jdthg.pdf](reports/final/Recomendaciones_Reto4_jdthg.pdf)

---

## 🛠️ Tecnologías utilizadas

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/pandas-3.0-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas"/>
  <img src="https://img.shields.io/badge/NumPy-2.x-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"/>
  <img src="https://img.shields.io/badge/Matplotlib-3.11-11557C?style=for-the-badge&logo=matplotlib&logoColor=white" alt="Matplotlib"/>
  <img src="https://img.shields.io/badge/Seaborn-0.13-4C72B0?style=for-the-badge" alt="Seaborn"/>
  <img src="https://img.shields.io/badge/MLxtend-2C3E50?style=for-the-badge" alt="MLxtend"/>
</p>

| Categoría | Herramientas |
|---|---|
| **Lenguaje** | Python 3.13 |
| **Datos** | pandas, NumPy, OpenPyXL |
| **ML** | scikit-learn, imbalanced-learn |
| **Reglas de asociación** | MLxtend (Apriori, FP-Growth) |
| **Visualización** | Matplotlib, Seaborn |
| **Documentación** | Pandoc, wkhtmltopdf |

---

## 📚 Documentación

| Documento | Enlace |
|---|---|
| 📄 **Informe Técnico completo (PDF)** | [Ver informe](reports/final/Informe_Tecnico_Reto4_jdthg.pdf) |
| 📝 **Informe Técnico (MD)** | [Ver informe](reports/final/Informe_Tecnico_Reto4_jdthg.md) |
| 🌐 **Informe Técnico (HTML)** | [Ver informe](reports/final/Informe_Tecnico_Reto4_jdthg.html) |
| 💼 **Recomendaciones de negocio (PDF)** | [Ver recomendaciones](reports/final/Recomendaciones_Reto4_jdthg.pdf) |
| 🎤 **Presentación PowerPoint** | [Ver presentación](reports/final/Presentacion-Reto-4-Data-Mining-aplicado-a-Pobreza-Infantil.pptx) |
| 📦 **Paquete completo (tar.gz)** | [Descargar](reports/final/Reto4_DataMining_PobrezaInfantil_jdthg.tar.gz) |

---

## ⚠️ Limitaciones

1. **Cobertura limitada de variables de pobreza infantil** (~0,5%).
2. Se usó `under5_mortality_rate` como **proxy** (cobertura 82%).
3. **Correlación ≠ causalidad**: los hallazgos son asociaciones estadísticas, no relaciones causales.
4. **Requiere reentrenamiento anual** por deriva de datos.

---

## 🔄 Próximas mejoras

- [ ] Añadir datos más recientes (2025+)
- [ ] Incorporar variables cualitativas (índice de desarrollo humano, gobernanza)
- [ ] Análisis temporal de la evolución por país
- [ ] Modelos de series temporales (SARIMA, Prophet)
- [ ] Dashboard interactivo con Streamlit o Power BI
- [ ] API REST para consulta de predicciones

---

## 👤 Autora

**Judit Giravent Pineda**

- Business Analytics Student | Odisea Data
- GitHub: [@jdthgp27](https://github.com/jdthgp27)
- LinkedIn: [linkedin.com/in/judit-giravent-27b167156](https://linkedin.com/in/judit-giravent-27b167156)
- Email: jdthgp27@gmail.com

---

## 📜 Licencia

MIT License — ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- [UNICEF Data](https://data.unicef.org/)
- [World Bank Open Data](https://data.worldbank.org/)
- [Odisea Data](https://odiseadata.com/) — Programa de formación

---

⭐ Si este proyecto te resulta útil, ¡dale una estrella!