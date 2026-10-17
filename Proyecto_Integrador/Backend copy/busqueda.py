"""
Algoritmos de búsqueda de rutas y cálculo de transbordos/costos.
- BFS para encontrar caminos y minimizar transbordos.
- Lógica de cobertura de tramos por rutas reales.
"""

from grafo import grafo
from datos import rutas


def buscar_ruta(origen, destino):
    """BFS: encuentra un camino más corto en número de paradas."""
    if origen not in grafo or destino not in grafo:
        return None

    visitados = set()
    pendientes = [[origen]]

    while pendientes:
        camino = pendientes.pop(0)
        actual = camino[-1]

        if actual == destino:
            return camino

        if actual not in visitados:
            visitados.add(actual)
            for vecino in grafo.get(actual, []):
                if vecino not in visitados:
                    pendientes.append(camino + [vecino])

    return None


def buscar_rutas(origen, destino, max_rutas=10):
    """
    BFS que encuentra varios caminos sin ciclos.
    Limita el número de resultados para el prototipo.
    """
    if origen not in grafo or destino not in grafo:
        return []

    pendientes = [[origen]]
    rutas_encontradas = []

    while pendientes and len(rutas_encontradas) < max_rutas:
        camino = pendientes.pop(0)
        actual = camino[-1]

        if actual == destino:
            rutas_encontradas.append(camino)
        else:
            for vecino in grafo.get(actual, []):
                if vecino not in camino:  # evita ciclos
                    pendientes.append(camino + [vecino])

    return rutas_encontradas


def tramo_cubierto(camino, inicio, fin, paraderos_ruta):
    """
    Verifica si el sub-camino camino[inicio:fin+1] está cubierto
    de forma consecutiva por una misma ruta (mismo sentido o inverso).
    """
    for i in range(inicio, fin):
        actual = camino[i]
        siguiente = camino[i + 1]

        if actual not in paraderos_ruta or siguiente not in paraderos_ruta:
            return False

        pos_actual = paraderos_ruta.index(actual)
        pos_siguiente = paraderos_ruta.index(siguiente)

        if abs(pos_actual - pos_siguiente) != 1:
            return False

    return True


def minimo_buses(camino):
    """
    Calcula el número mínimo de buses (rutas) necesarios para cubrir un camino.
    Usa programación dinámica hacia atrás.
    Retorna None si no es posible cubrir el camino con las rutas disponibles.
    """
    cantidad = len(camino)

    if cantidad < 2:
        return 0

    minimo = [float("inf")] * cantidad
    minimo[-1] = 0

    for inicio in range(cantidad - 2, -1, -1):
        for fin in range(inicio + 1, cantidad):
            for ruta in rutas:
                paraderos_ruta = ruta["paraderos"]
                if tramo_cubierto(camino, inicio, fin, paraderos_ruta):
                    if minimo[fin] != float("inf"):
                        minimo[inicio] = min(minimo[inicio], 1 + minimo[fin])

    if minimo[0] == float("inf"):
        return None

    return minimo[0]


def obtener_rutas_usadas(camino):
    """
    Devuelve la lista de nombres de rutas que cubren el camino
    con el menor número de transbordos posible.
    """
    cantidad = len(camino)
    if cantidad < 2:
        return []

    minimo = [float("inf")] * cantidad
    minimo[-1] = 0
    decision = [None] * cantidad  # (fin, nombre_ruta)

    for inicio in range(cantidad - 2, -1, -1):
        for fin in range(inicio + 1, cantidad):
            for ruta in rutas:
                if tramo_cubierto(camino, inicio, fin, ruta["paraderos"]):
                    if minimo[fin] != float("inf"):
                        candidato = 1 + minimo[fin]
                        if candidato < minimo[inicio]:
                            minimo[inicio] = candidato
                            decision[inicio] = (fin, ruta["nombre"])

    if minimo[0] == float("inf"):
        return []

    rutas_usadas = []
    i = 0
    while i < cantidad - 1 and decision[i] is not None:
        fin, nombre = decision[i]
        rutas_usadas.append(nombre)
        i = fin

    return rutas_usadas


def calcular_costo(rutas_usadas):
    """Suma el costo de cada ruta utilizada (una vez por cada bus)."""
    if not rutas_usadas:
        return 0

    costos = {r["nombre"]: r["costo"] for r in rutas}
    return sum(costos.get(nombre, 0) for nombre in rutas_usadas)