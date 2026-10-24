from solid.lsp_liskov_substitution import bad, good


def make_fly(birds: list) -> None:
    for b in birds:
        print(" ", b.fly())


def stretch(rect: bad.Rectangle) -> float:
    rect.set_width(5)
    rect.set_height(4)
    return rect.area()  # callers expect 20


def run() -> None:
    print("=== LSP: Bird & Rectangle/Square ===")
    print("--- Violation ---")
    try:
        make_fly([bad.Sparrow(), bad.Penguin()])
    except NotImplementedError as e:
        print("  Penguin broke code written for Bird:", e)
    print("  Rectangle area expected 20, got", stretch(bad.Rectangle(1, 1)))
    print("  Square area expected 20, got", stretch(bad.Square(1, 1)))

    print("--- Refactored ---")
    for b in (good.Sparrow(), good.Eagle(), good.Penguin()):
        print(" ", b.move())
    for s in (good.Rectangle(5, 4), good.Square(4)):
        print(f"  {s} area={s.area()}")


if __name__ == "__main__":
    run()
