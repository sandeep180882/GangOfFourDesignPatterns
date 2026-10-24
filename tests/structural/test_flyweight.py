from patterns.structural.flyweight.pattern import IconFactory, MapLayer


def test_factory_returns_same_flyweight():
    f = IconFactory()
    assert f.get("hotel", "blue") is f.get("hotel", "blue")
    assert f.get("hotel", "red") is not f.get("hotel", "blue")
    assert f.count == 2


def test_many_markers_share_few_icons():
    layer = MapLayer()
    for i in range(1000):
        layer.add(i, i, f"m{i}", "atm", "green" if i % 2 else "red")
    assert len(layer.markers) == 1000
    assert layer.factory.count == 2
    assert layer.icon_memory_bytes() * 400 < layer.unshared_memory_bytes()


def test_extrinsic_state_is_per_marker():
    layer = MapLayer()
    a = layer.add(1, 2, "A", "fuel", "orange")
    b = layer.add(3, 4, "B", "fuel", "orange")
    assert a.icon is b.icon
    assert a.draw() != b.draw()
