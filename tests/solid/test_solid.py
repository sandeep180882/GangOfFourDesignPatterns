import pytest

from solid.dip_dependency_inversion import bad as dip_bad, good as dip_good
from solid.isp_interface_segregation import good as isp_good
from solid.lsp_liskov_substitution import bad as lsp_bad, good as lsp_good
from solid.ocp_open_closed import bad as ocp_bad, good as ocp_good
from solid.putting_it_together import system
from solid.srp_single_responsibility import good as srp


# SRP
def test_srp_calculator_independent_of_printing():
    inv = srp.Invoice(1, "Ada", [srp.LineItem("a", 10.0, 2)])
    assert srp.InvoiceCalculator(0.1).total(inv) == 22.0


def test_srp_new_printer_needs_no_other_change():
    inv = srp.Invoice(1, "Ada", [srp.LineItem("a", 10.0, 1)])
    assert "<h1>" in srp.HtmlInvoicePrinter().render(inv, 11.0)
    mailer = srp.InvoiceMailer()
    mailer.send("x@y.z", "hi")
    assert mailer.outbox == ["To: x@y.z\nhi"]


# OCP
def test_ocp_bad_rejects_new_type():
    with pytest.raises(ValueError):
        ocp_bad.DiscountEngine().apply("student", 100)


def test_ocp_good_extends_by_registration():
    engine = ocp_good.DiscountEngine()
    with pytest.raises(ValueError):
        engine.apply("student", 100)
    engine.register("student", ocp_good.StudentDiscount())
    assert engine.apply("student", 100) == pytest.approx(85)
    assert engine.apply("regular", 100) == 100


# LSP
@pytest.mark.parametrize("cls", lsp_good.concrete_subclasses(lsp_good.Bird))
def test_lsp_every_bird_can_move(cls):
    assert isinstance(cls().move(), str)


@pytest.mark.parametrize("cls", lsp_good.concrete_subclasses(lsp_good.FlyingBird))
def test_lsp_every_flying_bird_can_fly(cls):
    assert "flies" in cls().fly()


def test_lsp_shape_contract_over_all_subclasses():
    subs = lsp_good.concrete_subclasses(lsp_good.Shape)
    assert len(subs) == 2
    assert lsp_good.Rectangle(2, 3).area() == 6
    assert lsp_good.Square(3).area() == 9


def test_lsp_violations_in_bad_hierarchy():
    with pytest.raises(NotImplementedError):
        lsp_bad.Penguin().fly()
    r = lsp_bad.Square(1, 1)
    r.set_width(5)
    r.set_height(4)
    assert r.area() != 20


# ISP
def test_isp_old_printer_only_prints():
    old = isp_good.OldPrinter()
    assert isinstance(old, isp_good.Printer)
    assert not isinstance(old, isp_good.Scanner)
    assert not isinstance(old, isp_good.Fax)


def test_isp_scan_all_skips_non_scanners():
    devices = [isp_good.OldPrinter(), isp_good.MultiFunctionPrinter()]
    assert isp_good.scan_all(devices) == ["scanned page"]


# DIP
def test_dip_bad_cannot_run_without_infrastructure():
    with pytest.raises(ConnectionError):
        dip_bad.OrderService().place_order("a", "b")


def test_dip_good_with_injected_fakes():
    repo, notifier = dip_good.InMemoryRepository(), dip_good.FakeNotifier()
    dip_good.OrderService(repo, notifier).place_order("ada", "book")
    assert repo.orders == [{"customer": "ada", "item": "book"}]
    assert notifier.sent == [("ada", "Order for book confirmed")]


# Capstone
def test_checkout_happy_path():
    log: list[str] = []
    facade, email, inventory = system.build_default_checkout(log)
    receipt = facade.checkout("ada", ["laptop", "mouse"], "vip")
    assert receipt.total == pytest.approx(660.0)
    assert inventory.reserved == ["laptop", "mouse"]
    assert email.sent and log == ["charged card:ada:660.00"]


def test_checkout_fraud_decorator_blocks_and_skips_events():
    facade, email, _ = system.build_default_checkout()
    with pytest.raises(ValueError, match="fraud"):
        facade.checkout("bob", ["laptop", "laptop"])
    assert email.sent == []
    with pytest.raises(ValueError):
        system.discount_factory("bogus")
