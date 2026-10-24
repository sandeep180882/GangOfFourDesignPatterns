from concurrent.futures import ThreadPoolExecutor

from patterns.creational.singleton.pattern import ConfigManager


def run() -> None:
    print("=== Singleton: Config Manager ===")
    ConfigManager.reset()

    db_module = ConfigManager()
    api_module = ConfigManager()
    print(f"db_module is api_module: {db_module is api_module}")

    db_module.set("debug", True)
    print(f"api_module sees debug = {api_module.get('debug')} (change made via db_module)")

    with ThreadPoolExecutor(max_workers=8) as pool:
        ids = {id(c) for c in pool.map(lambda _: ConfigManager(), range(50))}
    print(f"50 concurrent requests -> {len(ids)} distinct instance(s)")
    print(f"Settings were loaded {ConfigManager.load_count} time(s)")


if __name__ == "__main__":
    run()
