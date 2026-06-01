from __future__ import annotations

import argparse
import sys

from awtrix.client import AwtrixClient, AwtrixConnectionError
from awtrix.config import ConfigManager
from awtrix.i18n import I18n
from cli.init_flow import run_init
import cli.commands.apps as cmd_apps
import cli.commands.display as cmd_display
import cli.commands.notify as cmd_notify
import cli.commands.power as cmd_power


def _build_parser(i18n: I18n) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="awtrix",
        description=i18n.t("help_prog_desc"),
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    sub.add_parser("init",  help=i18n.t("help_init"))
    sub.add_parser("shell", help=i18n.t("help_shell"))

    p_status = sub.add_parser("status", help=i18n.t("help_status"))
    p_status.set_defaults(func=_handle_status)

    cmd_power.register(sub, i18n)
    cmd_display.register(sub, i18n)
    cmd_notify.register(sub, i18n)
    cmd_apps.register(sub, i18n)

    return parser


def _handle_status(args: argparse.Namespace, client: AwtrixClient, i18n: I18n) -> int:
    try:
        stats = client.get_stats()
        print(i18n.t("status_header"))
        print(f"  {i18n.t('status_version')} {stats.version}")
        print(f"  {i18n.t('status_battery')} {stats.battery}%")
        print(f"  {i18n.t('status_ram')}     {stats.ram} bytes")
        print(f"  {i18n.t('status_uptime')}  {stats.uptime}s")
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1


def main() -> None:
    config = ConfigManager()
    i18n = I18n(config.config.language)

    parser = _build_parser(i18n)
    args = parser.parse_args()

    if not config.config.is_initialized() or args.command == "init":
        run_init(config, i18n)
        return

    if args.command in (None, "shell"):
        from cli.repl import run_repl
        run_repl(config.config.device_ip, parser, i18n)
        return

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return

    ip = config.config.device_ip
    assert ip is not None
    try:
        with AwtrixClient(ip) as client:
            sys.exit(func(args, client, i18n))
    except KeyboardInterrupt:
        sys.exit(0)
