import random

from patterns.structural.flyweight.pattern import MapLayer


def run() -> None:
    print("=== Flyweight: Map Markers ===")
    rng = random.Random(42)
    layer = MapLayer()
    kinds = [("restaurant", "red"), ("hotel", "blue"), ("atm", "green"), ("fuel", "orange")]
    n = 100_000
    for i in range(n):
        kind, color = rng.choice(kinds)
        layer.add(rng.uniform(0, 1000), rng.uniform(0, 1000), f"POI-{i}", kind, color)

    print(f"Markers created      : {len(layer.markers):,}")
    print(f"Distinct icon objects: {layer.factory.count}")
    print(f"First marker         : {layer.markers[0].draw()}")
    shared, unshared = layer.icon_memory_bytes(), layer.unshared_memory_bytes()
    print(f"Icon memory, shared  : {shared:,} B")
    print(f"Icon memory, unshared: {unshared:,} B  (~{unshared // shared:,}x larger)")


if __name__ == "__main__":
    run()
