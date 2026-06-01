from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

LOCALES_DIR = Path(__file__).parent / "locales"
FALLBACK_LANG = "en"


class I18n:
    def __init__(self, language: Optional[str] = None) -> None:
        self._lang = language or FALLBACK_LANG
        self._strings: dict[str, str] = {}
        self._fallback: dict[str, str] = {}
        self._load()

    def _load_file(self, lang: str) -> dict[str, str]:
        path = LOCALES_DIR / f"{lang}.json"
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _load(self) -> None:
        self._fallback = self._load_file(FALLBACK_LANG)
        self._strings = (
            self._load_file(self._lang) if self._lang != FALLBACK_LANG else self._fallback
        )

    def set_language(self, lang: str) -> None:
        self._lang = lang
        self._load()

    def t(self, key: str, **kwargs: object) -> str:
        template = self._strings.get(key) or self._fallback.get(key, key)
        return template.format(**kwargs) if kwargs else template
