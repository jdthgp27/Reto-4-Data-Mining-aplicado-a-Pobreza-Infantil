#!/bin/bash
# Convertir los informes Markdown a PDF con Pandoc
# Requiere: pandoc + LaTeX (MiKTeX, TeX Live, o similar)

cd "$(dirname "$0")/.."

REPORTS_DIR="reports/final"

echo "==========================================="
echo "Generando PDFs desde Markdown"
echo "==========================================="

# Verificar pandoc
if ! command -v pandoc &> /dev/null; then
    echo "[ERROR] pandoc no esta instalado"
    echo "Instala con: choco install pandoc miktex -y"
    exit 1
fi

echo "[OK] pandoc encontrado"

# Convertir Informe Tecnico
echo ""
echo "--- Convirtiendo Informe Tecnico ---"
pandoc "$REPORTS_DIR/Informe_Tecnico_Reto4_jdthg.md" \
    -o "$REPORTS_DIR/Informe_Tecnico_Reto4_jdthg.pdf" \
    --pdf-engine=xelatex \
    -V geometry:margin=2cm \
    -V fontsize=11pt \
    -V lang=es \
    --toc \
    --toc-depth=2 \
    --highlight-style=tango \
    -V colorlinks=true \
    -V linkcolor=blue

if [ $? -eq 0 ]; then
    echo "[OK] Informe_Tecnico_Reto4_jdthg.pdf"
else
    echo "[ERROR] Fallo la conversion del informe tecnico"
fi

# Convertir Recomendaciones
echo ""
echo "--- Convirtiendo Recomendaciones ---"
pandoc "$REPORTS_DIR/Recomendaciones_Reto4_jdthg.md" \
    -o "$REPORTS_DIR/Recomendaciones_Reto4_jdthg.pdf" \
    --pdf-engine=xelatex \
    -V geometry:margin=2cm \
    -V fontsize=11pt \
    -V lang=es \
    --toc \
    --toc-depth=2 \
    --highlight-style=tango \
    -V colorlinks=true \
    -V linkcolor=blue

if [ $? -eq 0 ]; then
    echo "[OK] Recomendaciones_Reto4_jdthg.pdf"
else
    echo "[ERROR] Fallo la conversion de recomendaciones"
fi

echo ""
echo "==========================================="
echo "Conversion completada"
echo "==========================================="
ls -lh "$REPORTS_DIR"/*.pdf 2>/dev/null
