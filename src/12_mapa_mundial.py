"""
Genera un mapa mundial destacando los paises en situacion critica
"""
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from config import DATA_PROCESSED, FIGURES_DIR

# Cargar países con cluster asignado
df = pd.read_csv(DATA_PROCESSED / 'paises_con_cluster.csv')

# Quedarnos con el registro más reciente de cada país
df_reciente = df.sort_values('year').groupby('country_name').tail(1).copy()

# Añadir columna iso_alpha (código de 3 letras) para el mapa
# Si no tienes el iso2_code, lo inferimos del nombre
mapa_paises = {
    'Nigeria': 'NGA', 'Chad': 'TCD', 'Rwanda': 'RWA', 'Zambia': 'ZMB',
    'Central African Republic': 'CAF', 'Somalia': 'SOM', 'Mali': 'MLI',
    'Niger': 'NER', 'Burkina Faso': 'BFA', 'Mozambique': 'MOZ',
    'Guinea': 'GIN', 'Sierra Leone': 'SLE', 'Liberia': 'LBR',
    'South Sudan': 'SSD', 'Democratic Republic of the Congo': 'COD',
    'Uganda': 'UGA', 'Malawi': 'MWI', 'Burundi': 'BDI',
    'Togo': 'TGO', 'Benin': 'BEN', 'Madagascar': 'MDG',
    'Ethiopia': 'ETH', 'Tanzania': 'TZA', 'Cameroon': 'CMR',
    'Afghanistan': 'AFG', 'Yemen': 'YEM', 'Haiti': 'HTI',
    'Guinea-Bissau': 'GNB', 'Eritrea': 'ERI', 'Angola': 'AGO',
}

# Mapear
df_reciente['iso_alpha'] = df_reciente['country_name'].map(mapa_paises)

# Filtrar solo los que tienen iso_alpha (evita errores)
df_mapa = df_reciente.dropna(subset=['iso_alpha']).copy()

# Etiqueta legible
df_mapa['perfil'] = df_mapa['cluster'].map({
    0: 'Desarrollo relativo',
    1: 'Situación crítica'
})

# Mapa con Plotly
fig = px.choropleth(
    df_mapa,
    locations='iso_alpha',
    color='perfil',
    hover_name='country_name',
    hover_data={
        'gdp_per_capita_current_usd': ':,.0f',
        'under5_mortality_rate': ':.1f',
        'poverty_headcount_3_dollars_pct': ':.1f'
    },
    color_discrete_map={
        'Desarrollo relativo': '#3B82F6',  # azul
        'Situación crítica': '#DC2626'      # rojo
    },
    title='<b>Mapa mundial de pobreza infantil</b><br><sub>Segmentación por perfil socioeconómico (2024)</sub>'
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth',
        bgcolor='#F8FAFC'
    ),
    font=dict(family='Arial', size=14),
    title_font_size=20,
    legend_title_text='Perfil',
    width=1400,
    height=800,
    margin=dict(l=0, r=0, t=80, b=0)
)

# Guardar como PNG (requiere kaleido)
try:
    fig.write_image(FIGURES_DIR / 'mapa_mundial_pobreza.png', scale=2)
    print("[OK] Mapa guardado: reports/figures/mapa_mundial_pobreza.png")
except Exception as e:
    print(f"[WARN] No se pudo guardar PNG: {e}")
    print("[INFO] Guardando como HTML interactivo...")
    fig.write_html(FIGURES_DIR / 'mapa_mundial_pobreza.html')
    print("[OK] Mapa guardado: reports/figures/mapa_mundial_pobreza.html")

# Mostrar en pantalla
fig.show()
