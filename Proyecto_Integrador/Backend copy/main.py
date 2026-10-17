"""
Prototipo de consola del Sistema de Rutas de Buses y Colectivos de Fusagasugá.
Permite probar la lógica de backend antes de integrarla con el frontend.
"""

from datos import paraderos
from api import consultar_recorridos, listar_paraderos, listar_rutas


def mostrar_menu():
    print("=" * 55)
    print("  Sistema de Rutas — Fusagasugá (Prototipo Backend)")
    print("=" * 55)
    print("Paraderos disponibles:")
    for p in listar_paraderos():
        print(f"  • {p}")
    print()


def main():
    mostrar_menu()

    origen = input("Ingrese el paradero de origen: ").strip()
    destino = input("Ingrese el paradero de destino: ").strip()

    if origen not in paraderos:
        print(f"\nError: '{origen}' no es un paradero válido.")
        return
    if destino not in paraderos:
        print(f"\nError: '{destino}' no es un paradero válido.")
        return

    opciones = consultar_recorridos(origen, destino)

    if not opciones:
        print("\nNo se encontraron recorridos entre esos paraderos.")
        return

    print(f"\nSe encontraron {len(opciones)} opción(es):\n")

    for i, opcion in enumerate(opciones, start=1):
        print(f"── Opción {i} ──")
        print(f"  Recorrido   : {' → '.join(opcion['recorrido'])}")
        print(f"  Buses       : {opcion['buses']}")
        print(f"  Transbordos : {opcion['transbordos']}")
        print(f"  Rutas       : {', '.join(opcion['rutas_usadas']) or '—'}")
        print(f"  Costo       : ${opcion['costo']:,}")
        print()


if __name__ == "__main__":
    main()