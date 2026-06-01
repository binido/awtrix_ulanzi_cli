from __future__ import annotations

import argparse

from awtrix.client import AwtrixClient, AwtrixConnectionError
from awtrix.i18n import I18n


def register(sub: argparse._SubParsersAction, i18n: I18n) -> None:
    p_power = sub.add_parser("power", help=i18n.t("help_power"))
    p_power.add_argument("state", choices=["on", "off"])
    p_power.set_defaults(func=_handle_power)

    p_reboot = sub.add_parser("reboot", help=i18n.t("help_reboot"))
    p_reboot.set_defaults(func=_handle_reboot)


def _handle_power(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    try:
        client.set_power(args.state == "on")
        print(i18n.t("power_set", state=args.state))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1


def _handle_reboot(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    try:
        client.reboot()
        print(i18n.t("reboot_sent"))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1
