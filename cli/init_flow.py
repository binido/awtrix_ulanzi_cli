from __future__ import annotations

import re

from awtrix.client import AwtrixClient, AwtrixConnectionError, AwtrixNotFoundError
from awtrix.config import ConfigManager
from awtrix.i18n import I18n

_IP_PATTERN = re.compile(
    r"^(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\."
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\."
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\."
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)

_LANG_CHOICES: dict[str, str] = {"1": "en", "2": "ru"}


def _select_language(i18n: I18n, config: ConfigManager) -> None:
    print(i18n.t("select_language"))
    print(i18n.t("lang_option_en"))
    print(i18n.t("lang_option_ru"))
    while True:
        choice = input(i18n.t("lang_prompt")).strip()
        if choice in _LANG_CHOICES:
            lang = _LANG_CHOICES[choice]
            config.set_language(lang)
            i18n.set_language(lang)
            return
        print(i18n.t("lang_invalid"))


def _prompt_ip(i18n: I18n) -> str:
    while True:
        ip = input(i18n.t("enter_ip")).strip()
        if _IP_PATTERN.match(ip):
            return ip
        print(i18n.t("ip_invalid_format"))


def _probe_device(ip: str, i18n: I18n) -> bool:
    print(i18n.t("connecting", ip=ip))
    try:
        with AwtrixClient(ip) as client:
            stats = client.verify_device()
        print(i18n.t("connect_success"))
        if stats.version:
            print(i18n.t("device_version", version=stats.version))
        return True
    except AwtrixConnectionError as exc:
        reason = str(exc)
        if reason == "timeout":
            print(i18n.t("connect_timeout"))
        else:
            print(i18n.t("connect_error", error=reason))
        return False
    except AwtrixNotFoundError:
        print(i18n.t("connect_not_awtrix"))
        return False


def run_init(config: ConfigManager, i18n: I18n) -> None:
    print(i18n.t("welcome"))
    print()

    if config.config.language is None:
        _select_language(i18n, config)
        print()

    while config.config.device_ip is None:
        ip = _prompt_ip(i18n)
        if _probe_device(ip, i18n):
            config.set_device_ip(ip)
            print()
            print(i18n.t("config_saved"))
