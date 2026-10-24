"""Singleton: one thread-safe ConfigManager shared by the whole application."""
from __future__ import annotations

import threading
from typing import Any, ClassVar


class ConfigManager:
    """Singleton role: only one instance exists; `ConfigManager()` always returns it."""

    _instance: ClassVar[ConfigManager | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    load_count: ClassVar[int] = 0  # how many times settings were really loaded

    _settings: dict[str, Any]

    def __new__(cls) -> ConfigManager:
        if cls._instance is None:  # fast path, no lock once created
            with cls._lock:
                if cls._instance is None:  # double-checked locking
                    instance = super().__new__(cls)
                    instance._settings = instance._load()
                    cls._instance = instance
        return cls._instance

    @staticmethod
    def _load() -> dict[str, Any]:
        """Expensive step (file/env/remote read) that must run only once."""
        ConfigManager.load_count += 1
        return {"db_url": "postgres://localhost/shop", "debug": False, "timeout": 30}

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value

    @classmethod
    def reset(cls) -> None:
        """Drop the instance (test helper only)."""
        with cls._lock:
            cls._instance = None
            cls.load_count = 0
