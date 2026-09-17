"""
Genera un grafico de barras horizontal con el % de cobertura por columna
del dataset original. Util para la diapositiva de diagnostico.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_RAW, FIGURES_DIR, DATASET_NAME

print("Generando grafico de cobertura...")

# Cargar dataset original
df = pd.read_excel(DATA_RAW / DATASET_NAME)

# Calcular % de cobertura por columna
cobertura = (df.notna().sum() / len(df) * 100).sort_values(ascending=True)

# Filtrar solo columnas con algo de cobertura (evita las 100% vacías)
cobertura = cobertura[cobertura > 0]

# Limitar a las 25 columnas más representativas (o todas si son menos)
cobertura = cobertura.tail(25)

# Acortar nombres largos
def acortar(nombre, max_len=40):
    return nombre if len(nombre) <= max_len else nombre[:max_len-3] + '...'

etiquetas = [acortar(c) for c in cobertura.index]

# Colores: rojo si <50%, amarillo si 50-80%, verde si >80%
colores = []
for valor in cobertura.values:
    if valor < 50:
        colores.append('#DC2626')   # rojo
    elif valor < 80:
        colores.append('#F59E0B')   # amarillo
    else:
        colores.append('#10B981')   # verde

# Crear figura
fig, ax = plt.subplots(figsize=(14, 10))

bars = ax.barh(range(len(cobertura)), cobertura.values,
               color=colores, edgecolor='white', linewidth=0.5)

# Añadir etiquetas de porcentaje al final de cada barra
for i, (bar, valor) in enumerate(zip(bars, cobertura.values)):
    ax.text(valor + 1, bar.get_y() + bar.get_height()/2,
            f'{valor:.1f}%', va='center', fontsize=9, fontweight='bold')

# Configurar ejes
ax.set_yticks(range(len(cobertura)))
ax.set_yticklabels(etiquetas, fontsize=9)
ax.set_xlabel('% de datos no nulos', fontsize=11, fontweight='bold')
ax.set_xlim(0, 105)
ax.set_title('Cobertura de datos por columna en el dataset original',
             fontsize=14, fontweight='bold', pad=15)

# Líneas de referencia
ax.axvline(50, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.axvline(80, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.text(50, len(cobertura) - 0.5, ' 50%', color='gray', fontsize=8)
ax.text(80, len(cobertura) - 0.5, ' 80%', color='gray', fontsize=8)

# Grid
ax.grid(axis='x', alpha=0.3)

# Leyenda manual
from matplotlib.patches import Patch
leyenda = [
    Patch(facecolor='#10B981', label='Alta cobertura (>80%)'),
    Patch(facecolor='#F59E0B', label='Cobertura media (50-80%)'),
    Patch(facecolor='#DC2626', label='Baja cobertura (<50%)'),
]
ax.legend(handles=leyenda, loc='lower right', fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'diagnostico_cobertura.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"[OK] Grafico guardado: {FIGURES_DIR / 'diagnostico_cobertura.png'}")

# Mostrar resumen numérico
print(f"\nResumen de cobertura:")
print(f"  Columnas con >80% datos: {(cobertura > 80).sum()}")
print(f"  Columnas con 50-80% datos: {((cobertura >= 50) & (cobertura <= 80)).sum()}")
print(f"  Columnas con <50% datos: {(cobertura < 50).sum()}")
print(f"\nTop 5 columnas con mejor cobertura:")
for c, v in cobertura.tail(5).iloc[::-1].items():
    print(f"  {c}: {v:.1f}%")
