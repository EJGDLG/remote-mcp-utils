# maps_module.py
import folium
from folium.plugins import DualMap
from pathlib import Path

# Carpeta base del proyecto (un nivel arriba de este archivo)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Rutas a tus archivos geojson dentro de /data
GEOJSON_FILES = {
    "Atitlan": DATA_DIR / "Lago_Atitlan.geojson",
    "Amatitlan": DATA_DIR / "Lago_Amatitlan.geojson"
}

def build_dualmap(lake: str, period_a: str, period_b: str):
    """
    Genera un mapa comparativo entre dos periodos para un lago dado.
    - lake: "Atitlan" o "Amatitlan"
    - period_a: etiqueta de la capa izquierda (ej. "2020")
    - period_b: etiqueta de la capa derecha (ej. "2025")
    """
    if lake not in GEOJSON_FILES:
        raise ValueError(f"Lago no soportado: {lake}")

    geojson_file = GEOJSON_FILES[lake]
    if not geojson_file.exists():
        raise FileNotFoundError(f"No se encontró el archivo GeoJSON: {geojson_file}")

    # Crear un DualMap centrado en Guatemala
    m = DualMap(location=[14.6, -90.7], zoom_start=10)

    # Capa izquierda (periodo A)
    folium.GeoJson(
        str(geojson_file),
        name=f"{lake} - {period_a}",
        tooltip=f"{lake} - {period_a}"
    ).add_to(m.m1)

    # Capa derecha (periodo B)
    folium.GeoJson(
        str(geojson_file),
        name=f"{lake} - {period_b}",
        tooltip=f"{lake} - {period_b}"
    ).add_to(m.m2)

    folium.LayerControl().add_to(m.m1)
    folium.LayerControl().add_to(m.m2)

    # Guardar salida en archivo HTML dentro de /data
    out_file = DATA_DIR / f"dualmap_{lake.lower()}_{period_a}_{period_b}.html"
    m.save(str(out_file))

    return m, str(out_file)
