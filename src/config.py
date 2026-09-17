"""
Configuración del proyecto Reto 4 - Pobreza Infantil
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
FIGURES_DIR = BASE_DIR / "reports" / "figures"

for folder in [DATA_RAW, DATA_PROCESSED, MODELS_DIR, FIGURES_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.3

# Archivos del dataset
DATASET_NAME = "world_bank_gdp_data_with_poverty.xlsx"    # Dataset principal
COUNTRIES_FILE = "world_bank_countries.csv"               # Referencia de países
NUTRITION_FILE = "nutrition_data.csv"                     # Nutrición infantil
