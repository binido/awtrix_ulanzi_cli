from __future__ import annotations

import argparse

from awtrix.client import AwtrixClient, AwtrixConnectionError
from awtrix.i18n import I18n


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("notify", help="Send a notification to the device")
    p.add_argument("text", help="Text to display")
    p.add_argument("--color", nargs=3, type=int, metavar=("R", "G", "B"),
                   help="Text color (default: white)")
    p.add_argument("--bg-color", nargs=3, type=int, metavar=("R", "G", "B"),
                   help="Background color")
    p.add_argument("--duration", type=int, default=5, metavar="SEC",
                   help="Display duration in seconds (default: 5)")
    p.add_argument("--repeat", type=int, default=1, metavar="N",
                   help="Number of times to repeat (default: 1)")
    p.add_argument("--rainbow", action="store_true",
                   help="Enable rainbow text color effect")
    p.add_argument("--icon", metavar="NAME",
                   help="Icon name from the device icon set")
    p.add_argument("--sound", metavar="FILE",
                   help="Sound file to play (RTTTL or MP3 name)")
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
