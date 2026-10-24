from concurrent.futures import ThreadPoolExecutor

import pytest

from patterns.creational.singleton.pattern import ConfigManager


@pytest.fixture(autouse=True)
def _reset():
    ConfigManager.reset()
    yield
    ConfigManager.reset()


def test_same_instance_and_shared_state():
    a, b = ConfigManager(), ConfigManager()
    assert a is b
    a.set("x", 1)
    assert b.get("x") == 1


def test_thread_safe_single_load():
    with ThreadPoolExecutor(max_workers=16) as pool:
        ids = {id(c) for c in pool.map(lambda _: ConfigManager(), range(200))}
    assert len(ids) == 1
    assert ConfigManager.load_count == 1
