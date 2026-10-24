"""CLI runner: `python main.py` for a menu, `python main.py <id|all>` to run directly."""

from __future__ import annotations

import sys

from catalog import Demo, discover, find


def _print_menu(demos: list[Demo]) -> None:
    group = ""
    for index, demo in enumerate(demos, 1):
        if demo.group != group:
            group = demo.group
            print(f"\n[{group}]")
        print(f"  {index:>2}. {demo.name:<28} ({demo.id})")
    print("\n   a. run all     q. quit")


def main(argv: list[str]) -> int:
    demos = discover()
    if argv:
        targets = demos if argv[0] == "all" else [d for d in [find(argv[0])] if d]
        if not targets:
            print(f"Unknown demo '{argv[0]}'. Run without arguments to list demos.")
            return 1
        for demo in targets:
            print(demo.run())
        return 0

    while True:
        _print_menu(demos)
        choice = input("\nPick a number: ").strip().lower()
        if choice in {"q", "quit", ""}:
            return 0
        if choice == "a":
            for demo in demos:
                print(demo.run())
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            print(demos[int(choice) - 1].run())
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
