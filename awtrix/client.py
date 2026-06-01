from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import requests

DEFAULT_TIMEOUT = 5


class AwtrixConnectionError(Exception):
    """Raised when the device is unreachable or the request fails."""


class AwtrixNotFoundError(Exception):
    """Raised when the target host is reachable but is not an AWTRIX device."""


@dataclass
class DeviceStats:
    battery: Optional[int]
    ram: Optional[int]
    uptime: Optional[int]
    version: Optional[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeviceStats:
        return cls(
            battery=data.get("bat"),
            ram=data.get("ram"),
            uptime=data.get("uptime"),
            version=data.get("version"),
        )


class AwtrixClient:
    """HTTP client for the AWTRIX 3 device API."""

    def __init__(self, ip: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self._base_url = f"http://{ip}"
        self._timeout = timeout
        self._session = requests.Session()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, path: str) -> Any:
        url = f"{self._base_url}{path}"
        try:
            response = self._session.get(url, timeout=self._timeout)
            response.raise_for_status()
            return response.json()
        except requests.Timeout as exc:
            raise AwtrixConnectionError("timeout") from exc
        except requests.ConnectionError as exc:
            raise AwtrixConnectionError("connection_error") from exc
        except requests.HTTPError as exc:
            raise AwtrixConnectionError(f"http_error:{exc.response.status_code}") from exc
        except ValueError as exc:
            raise AwtrixNotFoundError("invalid_json_response") from exc

    def _post(self, path: str, payload: Optional[dict[str, Any]] = None) -> None:
        url = f"{self._base_url}{path}"
        try:
            response = self._session.post(url, json=payload, timeout=self._timeout)
            response.raise_for_status()
        except requests.Timeout as exc:
            raise AwtrixConnectionError("timeout") from exc
        except requests.ConnectionError as exc:
            raise AwtrixConnectionError("connection_error") from exc
        except requests.HTTPError as exc:
            raise AwtrixConnectionError(f"http_error:{exc.response.status_code}") from exc

    # ------------------------------------------------------------------
    # Device info
    # ------------------------------------------------------------------

    def get_stats(self) -> DeviceStats:
        data = self._get("/api/stats")
        if not isinstance(data, dict):
            raise AwtrixNotFoundError("unexpected_response_type")
        return DeviceStats.from_dict(data)

    def verify_device(self) -> DeviceStats:
        """Probe the device and confirm it is an AWTRIX 3 instance."""
        stats = self.get_stats()
        if stats.version is None:
            raise AwtrixNotFoundError("version_field_missing")
        return stats

    def get_settings(self) -> dict[str, Any]:
        return self._get("/api/settings")

    def get_effects(self) -> list[str]:
        return self._get("/api/effects")

    def get_app_loop(self) -> list[Any]:
        return self._get("/api/loop")

    # ------------------------------------------------------------------
    # Device control
    # ------------------------------------------------------------------

    def update_settings(self, settings: dict[str, Any]) -> None:
        self._post("/api/settings", settings)

    def set_power(self, on: bool) -> None:
        self._post("/api/power", {"power": on})

    def reboot(self) -> None:
        self._post("/api/reboot")

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def next_app(self) -> None:
        self._post("/api/nextapp")

    def previous_app(self) -> None:
        self._post("/api/previousapp")

    def switch_app(self, name: str) -> None:
        self._post("/api/switch", {"name": name})

    # ------------------------------------------------------------------
    # Notifications & custom apps
    # ------------------------------------------------------------------

    def send_notification(self, payload: dict[str, Any]) -> None:
        self._post("/api/notify", payload)

    def dismiss_notification(self) -> None:
        self._post("/api/notify/dismiss")

    def push_custom_app(self, name: str, payload: dict[str, Any]) -> None:
        self._post(f"/api/custom?name={name}", payload)

    # ------------------------------------------------------------------
    # Indicators
    # ------------------------------------------------------------------

    def set_indicator(self, index: int, payload: dict[str, Any]) -> None:
        self._post(f"/api/indicator{index}", payload)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> AwtrixClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
