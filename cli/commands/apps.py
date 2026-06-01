from __future__ import annotations

import argparse

from awtrix.client import AwtrixClient, AwtrixConnectionError
from awtrix.i18n import I18n


def register(sub: argparse._SubParsersAction, i18n: I18n) -> None:
    p_app = sub.add_parser("app", help=i18n.t("help_app"))
    app_sub = p_app.add_subparsers(dest="app_cmd", metavar="<next|prev|list|switch>")

    app_sub.add_parser("next",   help=i18n.t("help_app_next")).set_defaults(func=_handle_next)
    app_sub.add_parser("prev",   help=i18n.t("help_app_prev")).set_defaults(func=_handle_prev)
    app_sub.add_parser("list",   help=i18n.t("help_app_list")).set_defaults(func=_handle_list)

    p_switch = app_sub.add_parser("switch", help=i18n.t("help_app_switch"))
    p_switch.add_argument("name", metavar="NAME")
    p_switch.set_defaults(func=_handle_switch)

    p_app.set_defaults(func=_handle_app_no_cmd)

    p_ind = sub.add_parser("indicator", help=i18n.t("help_indicator"))
    p_ind.add_argument("index", type=int, choices=[1, 2, 3], metavar="<1|2|3>")
    p_ind.add_argument("rgb_or_off", nargs="+", metavar="R G B | off",
                       help=i18n.t("help_indicator_rgb"))
    p_ind.add_argument("--blink", type=int, default=0, metavar="MS",
                       help=i18n.t("help_indicator_blink"))
    p_ind.add_argument("--fade", type=int, default=0, metavar="MS",
                       help=i18n.t("help_indicator_fade"))
    p_ind.set_defaults(func=_handle_indicator)


def _handle_next(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    try:
        client.next_app()
        print(i18n.t("app_next"))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1


def _handle_prev(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    try:
        client.previous_app()
        print(i18n.t("app_prev"))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1


def _handle_list(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    try:
        loop = client.get_app_loop()
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1

    if not loop:
        print(i18n.t("app_list_empty"))
        return 0
    for entry in loop:
        name = entry.get("name", "?") if isinstance(entry, dict) else str(entry)
        print(f"  - {name}")
    return 0


def _handle_switch(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    try:
        client.switch_app(args.name)
        print(i18n.t("app_switched", name=args.name))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1


def _handle_app_no_cmd(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    print(i18n.t("app_usage"))
    return 1


def _handle_indicator(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    parts = args.rgb_or_off

    if len(parts) == 1 and parts[0].lower() == "off":
        payload: dict = {"color": [0, 0, 0]}
        state_label = i18n.t("indicator_off")
    elif len(parts) == 3:
        try:
            color = [int(p) for p in parts]
        except ValueError:
            print(i18n.t("indicator_invalid_color"))
            return 1
        if not all(0 <= c <= 255 for c in color):
            print(i18n.t("indicator_invalid_color"))
            return 1
        payload = {"color": color}
        if args.blink:
            payload["blink"] = args.blink
        if args.fade:
            payload["fade"] = args.fade
        state_label = str(color)
    else:
        print(i18n.t("indicator_invalid_args"))
        return 1

    try:
        client.set_indicator(args.index, payload)
        print(i18n.t("indicator_set", index=args.index, state=state_label))
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1
