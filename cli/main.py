from __future__ import annotations

import argparse
import sys

from awtrix.client import AwtrixClient, AwtrixConnectionError
from awtrix.config import ConfigManager
from awtrix.i18n import I18n
from cli.init_flow import run_init


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="awtrix",
        description="CLI utility for AWTRIX 3 / Ulanzi smart clock",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    sub.add_parser("init", help="Run the setup wizard")
    sub.add_parser("status", help="Show device stats")

    return parser


def _cmd_status(config: ConfigManager, i18n: I18n) -> int:
    ip = config.config.device_ip
    assert ip is not None  # guarded by caller
    print(i18n.t("already_configured", ip=ip))
    try:
        with AwtrixClient(ip) as client:
            stats = client.get_stats()
        print(f"  Version : {stats.version}")
        print(f"  Battery : {stats.battery}%")
        print(f"  RAM     : {stats.ram} bytes free")
        print(f"  Uptime  : {stats.uptime}s")
        return 0
    except AwtrixConnectionError as exc:
        print(i18n.t("connect_error", error=str(exc)))
        return 1


def main() -> None:
    config = ConfigManager()
    i18n = I18n(config.config.language)

    parser = _build_parser()
    args = parser.parse_args()

    if not config.config.is_initialized() or args.command == "init":
        run_init(config, i18n)
        return

    if args.command == "status":
        sys.exit(_cmd_status(config, i18n))
    else:
        print(i18n.t("already_configured", ip=config.config.device_ip))
        parser.print_help()
