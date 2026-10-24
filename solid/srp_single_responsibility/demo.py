from solid.srp_single_responsibility.bad import Invoice as BadInvoice
from solid.srp_single_responsibility.good import (
    HtmlInvoicePrinter, Invoice, InvoiceCalculator, InvoiceMailer,
    InvoiceRepository, LineItem, TextInvoicePrinter,
)


def run() -> None:
    print("=== SRP: Invoice ===")
    print("--- Violation ---")
    bad = BadInvoice(1, "Ada", [("Keyboard", 50.0, 2)])
    methods = [m for m in ("total", "save", "render", "email") if hasattr(bad, m)]
    print(f"One class, {len(methods)} reasons to change: {methods}")
    print("New requirement 'HTML invoices' => edit Invoice.render, risking total()/save()/email().")
    print(bad.email("ada@example.com"))

    print("--- Refactored ---")
    invoice = Invoice(1, "Ada", [LineItem("Keyboard", 50.0, 2)])
    total = InvoiceCalculator().total(invoice)
    repo, mailer = InvoiceRepository(), InvoiceMailer()
    repo.save(invoice)
    print(mailer.send("ada@example.com", TextInvoicePrinter().render(repo.get(1), total)))
    print("HTML requirement: add HtmlInvoicePrinter, nothing else changes:")
    print(mailer.send("ada@example.com", HtmlInvoicePrinter().render(invoice, total)))


if __name__ == "__main__":
    run()
