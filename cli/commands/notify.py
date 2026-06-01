from __future__ import annotations

import argparse

from awtrix.client import AwtrixClient, AwtrixConnectionError
from awtrix.i18n import I18n


def register(sub: argparse._SubParsersAction, i18n: I18n) -> None:
    p = sub.add_parser("notify", help=i18n.t("help_notify"))
    p._example = i18n.t("example_notify")
    p.add_argument("text", help=i18n.t("help_notify_text"))
    p.add_argument("--color", nargs=3, type=int, metavar=("R", "G", "B"),
                   help=i18n.t("help_notify_color"))
    p.add_argument("--bg-color", nargs=3, type=int, metavar=("R", "G", "B"),
                   help=i18n.t("help_notify_bg_color"))
    p.add_argument("--duration", type=int, default=5, metavar="SEC",
                   help=i18n.t("help_notify_duration"))
    p.add_argument("--repeat", type=int, default=1, metavar="N",
                   help=i18n.t("help_notify_repeat"))
    p.add_argument("--rainbow", action="store_true",
                   help=i18n.t("help_notify_rainbow"))
    p.add_argument("--icon", metavar="NAME",
                   help=i18n.t("help_notify_icon"))
    p.add_argument("--sound", metavar="FILE",
                   help=i18n.t("help_notify_sound"))
    p.set_defaults(func=_handle)


def _handle(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    payload: dict = {
        "text": args.text,
        "duration": args.duration,
        "repeat": args.repeat,
        "rainbow": args.rainbow,
    }
    if args.color:
        payload["color"] = args.color
    if args.bg_color:
        payload["background"] = args.bg_color
    if args.icon:
        payload["icon"] = args.icon
    if args.sound:
        payload["sound"] = args.sound

    try:
        client.send_notification(payload)
        print(i18n.t("notify_sent"))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1
