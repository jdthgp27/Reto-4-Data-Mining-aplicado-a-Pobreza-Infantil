#!/bin/bash
cd "$(dirname "$0")/.."
PROJECT_DIR=$(pwd)
PKG="Reto4_DataMining_PobrezaInfantil_jdthg"
TMP="/tmp/$PKG"

echo "==========================================="
echo "Empaquetando entregables del Reto 4"
echo "==========================================="

rm -rf "$TMP"
mkdir -p "$TMP/01_codigo" "$TMP/02_informes" "$TMP/03_visualizaciones" "$TMP/04_modelos" "$TMP/05_datos"

echo "[1/6] Codigo fuente..."
cp src/*.py src/*.sh requirements.txt README.md "$TMP/01_codigo/" 2>/dev/null
echo "      $(ls "$TMP/01_codigo" | wc -l) archivos"

echo "[2/6] Informes..."
cp reports/final/*.md reports/final/*.pdf reports/final/*.html "$TMP/02_informes/" 2>/dev/null
echo "      $(ls "$TMP/02_informes" | wc -l) archivos"

echo "[3/6] Visualizaciones..."
cp reports/figures/*.png "$TMP/03_visualizaciones/" 2>/dev/null
echo "      $(ls "$TMP/03_visualizaciones" | wc -l) imagenes"

echo "[4/6] Modelos..."
cp models/*.pkl "$TMP/04_modelos/" 2>/dev/null
echo "      $(ls "$TMP/04_modelos" | wc -l) modelos"

echo "[5/6] Datos procesados..."
cp data/processed/*.csv data/processed/*.xlsx "$TMP/05_datos/" 2>/dev/null
echo "      $(ls "$TMP/05_datos" | wc -l) archivos"

echo "[6/6] LEEME.md..."
echo "# Reto 4: Data Mining aplicado a Pobreza Infantil" > "$TMP/LEEME.md"
echo "" >> "$TMP/LEEME.md"
echo "**Autor:** jdthg" >> "$TMP/LEEME.md"
echo "**Modulo:** BI y Big Data - Nivel 5" >> "$TMP/LEEME.md"
echo "" >> "$TMP/LEEME.md"
echo "## Contenido" >> "$TMP/LEEME.md"
echo "- 01_codigo/: Scripts Python del pipeline" >> "$TMP/LEEME.md"
echo "- 02_informes/: Informes en md, html, pdf" >> "$TMP/LEEME.md"
echo "- 03_visualizaciones/: 15 figuras PNG" >> "$TMP/LEEME.md"
echo "- 04_modelos/: RandomForest + Kmeans" >> "$TMP/LEEME.md"
echo "- 05_datos/: Datasets procesados" >> "$TMP/LEEME.md"
echo "" >> "$TMP/LEEME.md"
echo "## Hallazgo principal" >> "$TMP/LEEME.md"
echo "PIB bajo + Pobreza alta multiplica 6.4x el riesgo de mortalidad infantil." >> "$TMP/LEEME.md"

echo ""
echo "Comprimiendo..."
cd /tmp
if command -v zip &>/dev/null; then
    zip -rq "$PKG.zip" "$PKG"
    OUT="$PKG.zip"
else
    tar -czf "$PKG.tar.gz" "$PKG"
    OUT="$PKG.tar.gz"
fi
mv "/tmp/$OUT" "$PROJECT_DIR/reports/final/"
cd "$PROJECT_DIR"

echo ""
echo "==========================================="
echo "[OK] Paquete generado"
echo "==========================================="
ls -lh "reports/final/$OUT"
echo ""
echo "Contenido del paquete:"
echo "  codigo:          $(ls "$TMP/01_codigo" 2>/dev/null | wc -l) archivos"
echo "  informes:        $(ls "$TMP/02_informes" 2>/dev/null | wc -l) archivos"
echo "  visualizaciones: $(ls "$TMP/03_visualizaciones" 2>/dev/null | wc -l) imagenes"
echo "  modelos:         $(ls "$TMP/04_modelos" 2>/dev/null | wc -l) modelos"
echo "  datos:           $(ls "$TMP/05_datos" 2>/dev/null | wc -l) archivos"
rm -rf "$TMP"
