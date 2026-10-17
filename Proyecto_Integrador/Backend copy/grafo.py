"""
Construcción del grafo no dirigido a partir de las rutas.
Los nodos son paraderos; las aristas representan tramos consecutivos.
"""

from datos import rutas

grafo = {}

for ruta in rutas:
    paraderos_ruta = ruta["paraderos"]

    for i in range(len(paraderos_ruta) - 1):
        origen = paraderos_ruta[i]
        destino = paraderos_ruta[i + 1]

        if origen not in grafo:
            grafo[origen] = []
        if destino not in grafo:
            grafo[destino] = []

        if destino not in grafo[origen]:
            grafo[origen].append(destino)
        if origen not in grafo[destino]:
            grafo[destino].append(origen)