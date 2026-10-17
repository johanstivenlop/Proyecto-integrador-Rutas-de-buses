"""
API de consulta de recorridos — punto de entrada para el frontend.
Devuelve estructuras listas para serializar a JSON.
"""

from datos import paraderos, rutas
from busqueda import (
    buscar_rutas,
    minimo_buses,
    obtener_rutas_usadas,
    calcular_costo,
)


def listar_paraderos():
    """Lista de todos los paraderos disponibles."""
    return list(paraderos)


def listar_rutas():
    """Información de las rutas registradas."""
    return [
        {
            "nombre": r["nombre"],
            "paraderos": r["paraderos"],
            "costo": r["costo"],
        }
        for r in rutas
    ]


def consultar_recorridos(origen, destino):
    """
    Busca todos los recorridos posibles entre origen y destino.
    Retorna una lista de opciones ordenadas por número de buses
    (menos transbordos primero).
    """
    origen = origen.strip()
    destino = destino.strip()

    if origen not in paraderos or destino not in paraderos:
        return []

    if origen == destino:
        return [
            {
                "recorrido": [origen],
                "buses": 0,
                "transbordos": 0,
                "rutas_usadas": [],
                "costo": 0,
            }
        ]

    caminos = buscar_rutas(origen, destino)
    opciones = []

    for camino in caminos:
        buses = minimo_buses(camino)
        if buses is None:
            continue

        rutas_usadas = obtener_rutas_usadas(camino)
        costo = calcular_costo(rutas_usadas)

        opciones.append(
            {
                "recorrido": camino,
                "buses": buses,
                "transbordos": max(0, buses - 1),
                "rutas_usadas": rutas_usadas,
                "costo": costo,
            }
        )

    opciones.sort(key=lambda o: (o["buses"], len(o["recorrido"]), o["costo"]))
    return opciones