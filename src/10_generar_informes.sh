#!/bin/bash
# Generar HTML y PDF de los informes

cd "$(dirname "$0")/.."
REPORTS_DIR="reports/final"
TEMP_DIR=$(mktemp -d)

echo "==========================================="
echo "Generando HTML y PDF de los informes"
echo "==========================================="

# Verificar pandoc
if ! command -v pandoc &> /dev/null; then
    echo "[ERROR] pandoc no instalado"
    exit 1
fi
echo "[OK] pandoc encontrado"

# Detectar wkhtmltopdf (en PATH o ruta absoluta de Windows)
WKHTML=""
if command -v wkhtmltopdf &> /dev/null; then
    WKHTML="wkhtmltopdf"
    echo "[OK] wkhtmltopdf encontrado en PATH"
elif [ -f "/c/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe" ]; then
    WKHTML="/c/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    echo "[OK] wkhtmltopdf encontrado en Program Files"
else
    echo "[WARN] wkhtmltopdf NO encontrado - solo se generara HTML"
fi

# Crear CSS temporal
CSS_FILE="$TEMP_DIR/estilo.css"
cat > "$CSS_FILE" << 'CSS'
body { font-family: "Segoe UI", Arial, sans-serif; max-width: 900px;
       margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #333; }
h1 { color: #1a5490; border-bottom: 3px solid #1a5490; padding-bottom: 10px; }
h2 { color: #2c3e50; margin-top: 30px; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
h3 { color: #34495e; }
table { border-collapse: collapse; width: 100%; margin: 20px 0; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
th { background-color: #1a5490; color: white; }
tr:nth-child(even) { background-color: #f2f2f2; }
code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px;
       font-family: Consolas, monospace; font-size: 0.9em; }
pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
blockquote { border-left: 4px solid #1a5490; padding-left: 15px;
             color: #555; font-style: italic; background: #f9f9f9; }
CSS

# Procesar cada Markdown
for md_file in "$REPORTS_DIR"/*.md; do
    base=$(basename "$md_file" .md)
    html_file="$REPORTS_DIR/${base}.html"
    pdf_file="$REPORTS_DIR/${base}.pdf"

    echo ""
    echo "--- Procesando: $base ---"

    # MD -> HTML
    pandoc "$md_file" \
        -o "$html_file" \
        --standalone \
        --toc \
        --toc-depth=2 \
        --syntax-highlighting=tango \
        --metadata title="$base" \
        --css="$CSS_FILE" \
        --embed-resources

    if [ $? -eq 0 ]; then
        echo "[OK] HTML: $html_file"
    else
        echo "[ERROR] Fallo HTML de $base"
        continue
    fi

    # HTML -> PDF
    if [ -n "$WKHTML" ]; then
        "$WKHTML" \
            --enable-local-file-access \
            --page-size A4 \
            --margin-top 20mm \
            --margin-bottom 20mm \
            --margin-left 15mm \
            --margin-right 15mm \
            --footer-center "[page] / [topage]" \
            --footer-font-size 8 \
            --quiet \
            "$html_file" "$pdf_file"

        if [ $? -eq 0 ] && [ -f "$pdf_file" ]; then
            size=$(du -h "$pdf_file" | cut -f1)
            echo "[OK] PDF: $pdf_file ($size)"
        else
            echo "[ERROR] Fallo PDF de $base"
        fi
    fi
done

rm -rf "$TEMP_DIR"

echo ""
echo "==========================================="
echo "Proceso completado"
echo "==========================================="
ls -lh "$REPORTS_DIR"/
