from __future__ import annotations

import argparse
import json

from awtrix.client import AwtrixClient, AwtrixConnectionError
from awtrix.i18n import I18n


def register(sub: argparse._SubParsersAction, i18n: I18n) -> None:
    p_bri = sub.add_parser("brightness", help=i18n.t("help_brightness"))
    p_bri.add_argument("value", type=int, metavar="0-255", nargs="?", default=None)
    p_bri.add_argument("--auto", nargs="?", const="on", default=None, metavar="on|off",
                       help=i18n.t("help_brightness_auto"))
    p_bri._example = i18n.t("example_brightness")
    p_bri.set_defaults(func=_handle_brightness)

    p_settings = sub.add_parser("settings", help=i18n.t("help_settings"))
    settings_sub = p_settings.add_subparsers(dest="settings_cmd", metavar="<get|set>")

    p_get = settings_sub.add_parser("get", help=i18n.t("help_settings_get"))
    p_get.add_argument("key", nargs="?", default=None, metavar="KEY")
    p_get._example = i18n.t("example_settings_get")
    p_get.set_defaults(func=_handle_settings_get)

    p_set = settings_sub.add_parser("set", help=i18n.t("help_settings_set"))
    p_set.add_argument("key", metavar="KEY")
    p_set.add_argument("value", metavar="VALUE")
    p_set._example = i18n.t("example_settings_set")
    p_set.set_defaults(func=_handle_settings_set)

    p_settings.set_defaults(func=_handle_settings_no_cmd)


def _handle_brightness(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    has_value = args.value is not None
    has_auto  = args.auto is not None

    if not has_value and not has_auto:
        print(i18n.t("brightness_usage"))
        return 1

    if has_value and has_auto:
        print(i18n.t("brightness_conflict"))
        return 1

    if has_auto:
        enable = args.auto.lower() not in ("off", "false", "0")
        try:
            client.update_settings({"ABRI": enable})
            print(i18n.t("auto_brightness_set", state=args.auto.lower()))
            return 0
        except AwtrixConnectionError as exc:
            print(i18n.t("connect_error", error=str(exc)))
            return 1

    if not 0 <= args.value <= 255:
        print(i18n.t("brightness_range_error"))
        return 1
    try:
        client.update_settings({"BRI": args.value, "ABRI": False})
        print(i18n.t("brightness_set", value=args.value))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1


def _handle_settings_get(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    try:
        all_settings = client.get_settings()
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1

    if args.key:
        key = args.key.upper()
        if key not in all_settings:
            print(i18n.t("settings_key_not_found", key=key))
            return 1
        print(f"{key} = {all_settings[key]}")
    else:
        for k, v in sorted(all_settings.items()):
            print(f"  {k} = {v}")
    return 0


def _handle_settings_set(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    key = args.key.upper()
    value = _parse_value(args.value)
    try:
        client.update_settings({key: value})
        print(i18n.t("settings_set_ok", key=key, value=value))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1


def _handle_settings_no_cmd(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    print(i18n.t("settings_usage"))
    return 1


def _parse_value(raw: str) -> bool | int | float | list | str:
    lower = raw.lower()
    if lower in ("true", "yes", "on"):
        return True
    if lower in ("false", "no", "off"):
        return False
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw
