from solid.isp_interface_segregation import bad, good


def run() -> None:
    print("=== ISP: Multifunction printer ===")
    print("--- Violation ---")
    for m in (bad.MultiFunctionPrinter(), bad.OldPrinter()):
        try:
            print(f"  {type(m).__name__}.scan() ->", m.scan())
        except NotImplementedError as e:
            print(f"  {type(m).__name__}.scan() blew up:", e)

    print("--- Refactored ---")
    devices = [good.OldPrinter(), good.MultiFunctionPrinter()]
    print("  print_all:", good.print_all(devices, "report"))
    print("  scan_all (only Scanner-capable):", good.scan_all(devices))
    print("  OldPrinter is a Scanner?", isinstance(good.OldPrinter(), good.Scanner))


if __name__ == "__main__":
    run()
