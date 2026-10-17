"""
Datos del sistema de rutas de Fusagasugá.
Paraderos y rutas de ejemplo (prototipo).
"""

paraderos = [
    "Terminal",
    "Centro",
    "Hospital",
    "Alcaldía",
    "Universidad",
    "La pampa",
    "Plaza de Mercado",
]

rutas = [
    {
        "nombre": "Ruta 1",
        "paraderos": ["Terminal", "Centro", "Hospital", "Universidad"],
        "costo": 2600,
    },
    {
        "nombre": "Ruta 2",
        "paraderos": ["Terminal", "Alcaldía", "La pampa", "Universidad"],
        "costo": 2600,
    },
    {
        "nombre": "Ruta 3",
        "paraderos": ["La pampa", "Centro", "Alcaldía", "Plaza de Mercado"],
        "costo": 2600,
    },
]