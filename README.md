# ?? Reto 4: Data Mining aplicado a la Pobreza Infantil

> **An¨¢lisis avanzado de pobreza infantil en 217 pa¨ªses combinando clasificaci¨®n, clustering y reglas de asociaci¨®n para generar recomendaciones de pol¨ªtica p¨²blica basadas en datos.**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-orange.svg)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-3.0-red.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ?? Descripci¨®n

Este proyecto aplica **t¨¦cnicas avanzadas de Data Mining** sobre un dataset combinado del **Banco Mundial y UNICEF** (14.105 registros, 217 pa¨ªses, 1960-2024) para:

1. **Predecir** qu¨¦ pa¨ªses tienen alta mortalidad infantil
2. **Segmentar** pa¨ªses por perfil socioecon¨®mico
3. **Descubrir** reglas de asociaci¨®n entre indicadores
4. **Generar** recomendaciones accionables para pol¨ªticas p¨²blicas

Proyecto desarrollado como parte del m¨®dulo **BI y Big Data - Nivel 5** (Odisea Data).

---

## ?? Resultados principales

| T¨¦cnica | Algoritmo | M¨¦trica | Valor |
|---------|-----------|---------|-------|
| ?? **Clasificaci¨®n** | Random Forest | F1-Score | **0.9301** |
| ?? **Clustering** | K-means (K=2) | Silueta | **0.5370** |
| ?? **Asociaci¨®n** | FP-Growth | Lift m¨¢ximo | **6.37** |

### ?? Los 3 hallazgos clave

1. **El PIB per c¨¢pita es el predictor #1** (44.9% de importancia) de la mortalidad infantil alta
2. **Dos clusters claramente separados:** 82% desarrollo relativo vs 18% situaci¨®n cr¨ªtica
3. **La trampa de la pobreza es cuantificable:** PIB bajo + Pobreza alta ¡ú Mortalidad alta (lift=6.37)

---

## ?? Estructura del proyecto


reto4_pobreza_infantil/
©¦
©À©¤©¤ data/
©¦ ©À©¤©¤ raw/ # Dataset original (Banco Mundial + UNICEF)
©¦ ©¸©¤©¤ processed/ # Datos limpios y resultados
©¦
©À©¤©¤ models/ # Modelos entrenados (.pkl)
©¦ ©À©¤©¤ mejor_modelo_clasificacion.pkl
©¦ ©¸©¤©¤ kmeans_clustering.pkl
©¦
©À©¤©¤ reports/
©¦ ©À©¤©¤ figures/ # 15 visualizaciones PNG
©¦ ©¸©¤©¤ final/ # Informes finales (MD/HTML/PDF)
©¦
©À©¤©¤ src/ # Pipeline completo en Python
©¦ ©À©¤©¤ 01_exploracion.py
©¦ ©À©¤©¤ 02_diagnostico.py
©¦ ©À©¤©¤ 03_preparacion.py
©¦ ©À©¤©¤ 04_clasificacion.py
©¦ ©À©¤©¤ 05_clustering.py
©¦ ©À©¤©¤ 06_asociacion.py
©¦ ©À©¤©¤ 07_evaluacion_interpretacion.py
©¦ ©À©¤©¤ 08_recomendaciones.py
©¦ ©¸©¤©¤ 09_informe_tecnico.py
©¦
©À©¤©¤ requirements.txt
©¸©¤©¤ README.md


---

## ?? Instalaci¨®n y uso

### Requisitos previos

- Python 3.11+
- pip
- Git

### Instalaci¨®n

```bash
git clone https://github.com/jdthgp27/Reto-4-Data-Mining-aplicado-a-Pobreza-Infantil.git
cd Reto-4-Data-Mining-aplicado-a-Pobreza-Infantil

python -m venv .venv
source .venv/Scripts/activate    # Windows (Git Bash)
# source .venv/bin/activate      # Linux/Mac

pip install -r requirements.txt

# Exploraci¨®n y preparaci¨®n
python src/01_exploracion.py
python src/02_diagnostico.py
python src/03_preparacion.py

# T¨¦cnicas de Data Mining
python src/04_clasificacion.py
python src/05_clustering.py
python src/06_asociacion.py

# Evaluaci¨®n e interpretaci¨®n
python src/07_evaluacion_interpretacion.py
python src/08_recomendaciones.py
python src/09_informe_tecnico.py

?? Dataset
Fuente: world-bank-unicef-data

Archivo principal: world_bank_gdp_data_with_poverty.xlsx

Origen: Banco Mundial + UNICEF

Caracter¨ªsticas
14.105 registros (pa¨ªs ¡Á a?o)

217 pa¨ªses representados

64 columnas (econ¨®micas, fiscales, pobreza, mortalidad, nutrici¨®n)

Periodo: 1960-2024

?? Metodolog¨ªa
1?? Clasificaci¨®n
Predicci¨®n binaria de high_child_mortality usando:

¨¢rbol de Decisi¨®n (interpretabilidad)

Random Forest (ganador: F1=0.93)

SVM (kernel RBF)

Features clave: PIB per c¨¢pita, bajo peso al nacer, pobreza extrema

2?? Clustering
Segmentaci¨®n con K-means, DBSCAN y clustering jer¨¢rquico.

K ¨®ptimo: 2 clusters (m¨¦todo del codo + silueta)

3?? Asociaci¨®n
Reglas con Apriori y FP-Growth (soporte ¡Ý 5%, confianza ¡Ý 60%, lift > 1.1).

Resultado: 85 reglas, siendo la m¨¢s fuerte GDP_Bajo + Pob_Alta ¡ú Mort_Alta

?? Visualizaciones destacadas
Dashboard final
https://reports/figures/dashboard_final.png

Matriz de correlaciones
https://reports/figures/matriz_correlaciones.png

Importancia de features
https://reports/figures/clasificacion_importancia.png

Segmentaci¨®n de pa¨ªses
https://reports/figures/clustering_pca_comparativa.png

(15 visualizaciones completas en reports/figures/)


?? Recomendaciones de negocio
R1 - Pa¨ªses con desarrollo relativo: Programas de prevenci¨®n temprana

R2 - Pa¨ªses en situaci¨®n cr¨ªtica: Intervenci¨®n humanitaria integral

R3 - Sistema de alerta temprana: Basado en PIB bajo + pobreza alta

R4 - Optimizaci¨®n presupuestaria: Priorizar desarrollo econ¨®mico

R5 - Monitoreo continuo: Pipeline predictivo anual

?? Detalles en reports/final/Recomendaciones_Reto4_jdthg.pdf

??? Tecnolog¨ªas utilizadas
Categor¨ªa	Herramientas
Lenguaje	Python 3.13
Datos	Pandas, NumPy, OpenPyXL
ML	Scikit-learn, Imbalanced-learn
Reglas de asociaci¨®n	MLxtend
Visualizaci¨®n	Matplotlib, Seaborn
Documentaci¨®n	Pandoc, wkhtmltopdf


?? Documentaci¨®n
?? Informe T¨¦cnico completo

?? Recomendaciones de negocio

?? Limitaciones
Cobertura limitada de variables de pobreza infantil (~0.5%)

Se us¨® under5_mortality_rate como proxy (cobertura 82%)

Correlaci¨®n ¡Ù causalidad

Requiere reentrenamiento anual por deriva de datos

?? Licencia
MIT License - ver LICENSE para m¨¢s detalles.

?? Autor
Judit Giravent

Proyecto del m¨®dulo BI y Big Data - Nivel 5

? Si este proyecto te resulta ¨²til, ?dale una estrella!

?? Agradecimientos
UNICEF Data

World Bank Open Data

Odisea Data - Programa de formaci¨®n