#!/bin/bash
# Convertir Markdown a HTML estilizado (sin LaTeX)

cd "$(dirname "$0")/.."
REPORTS_DIR="reports/final"

CSS='<style>
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
</style>'

for md_file in "$REPORTS_DIR"/*.md; do
    base=$(basename "$md_file" .md)
    html_file="$REPORTS_DIR/${base}.html"

    echo "Convirtiendo $md_file..."
    pandoc "$md_file" \
        -o "$html_file" \
        --standalone \
        --toc \
        --toc-depth=2 \
        --highlight-style=tango \
        --metadata title="$base" \
        -H <(echo "$CSS")

    if [ $? -eq 0 ]; then
        echo "[OK] $html_file"
    fi
done

echo ""
echo "Abre los HTML en Chrome y usa Ctrl+P para exportar a PDF"
