from patterns.structural.facade.pattern import OrderFacade


def test_successful_order_coordinates_subsystems():
    shop = OrderFacade()
    r = shop.place_order("alice", "mouse", 2)
    assert r.success and r.tracking_id
    assert shop.inventory.stock["mouse"] == 18
    assert len(shop.email.sent) == 1


def test_out_of_stock_short_circuits():
    shop = OrderFacade()
    r = shop.place_order("bob", "laptop", 99)
    assert not r.success
    assert shop.email.sent == []


def test_payment_decline_releases_stock():
    shop = OrderFacade()
    r = shop.place_order("carol", "laptop", 5)  # 6000 > limit
    assert not r.success and r.message == "payment declined"
    assert shop.inventory.stock["laptop"] == 5
    assert "declined" in shop.email.sent[0]
