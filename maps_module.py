# maps_module.py
import folium
from folium.plugins import DualMap
import os

# Rutas a tus archivos geojson
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GEOJSON_FILES = {
    "Atitlan": os.path.join(BASE_DIR, "Lago_Atitlan.geojson"),
    "Amatitlan": os.path.join(BASE_DIR, "Lago_Amatitlan.geojson")
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

    # Crear un DualMap
    m = DualMap(location=[14.6, -90.7], zoom_start=10)

    # Capa izquierda (periodo A)
    folium.GeoJson(
        geojson_file,
        name=f"{lake} - {period_a}",
        tooltip=f"{lake} - {period_a}"
    ).add_to(m.m1)

    # Capa derecha (periodo B)
    folium.GeoJson(
        geojson_file,
        name=f"{lake} - {period_b}",
        tooltip=f"{lake} - {period_b}"
    ).add_to(m.m2)

    folium.LayerControl().add_to(m.m1)
    folium.LayerControl().add_to(m.m2)

    # Guardar salida en archivo HTML
    out_file = os.path.join(BASE_DIR, f"dualmap_{lake.lower()}_{period_a}_{period_b}.html")
    m.save(out_file)

    return m, out_file
