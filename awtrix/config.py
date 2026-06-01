from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Optional

CONFIG_PATH = Path(__file__).parent.parent / "config.json"


@dataclass
class Config:
    language: Optional[str] = None
    device_ip: Optional[str] = None

    def is_initialized(self) -> bool:
        return self.language is not None and self.device_ip is not None


class ConfigManager:
    def __init__(self, path: Path = CONFIG_PATH) -> None:
        self._path = path
        self._config = self._load()

    def _load(self) -> Config:
        if not self._path.exists():
            return Config()
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            valid_keys = {f.name for f in fields(Config)}
            return Config(**{k: v for k, v in data.items() if k in valid_keys})
        except (json.JSONDecodeError, TypeError):
            return Config()

    def save(self) -> None:
        self._path.write_text(
            json.dumps(asdict(self._config), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @property
    def config(self) -> Config:
        return self._config

    def set_language(self, lang: str) -> None:
        self._config.language = lang
        self.save()

    def set_device_ip(self, ip: str) -> None:
        self._config.device_ip = ip
        self.save()
