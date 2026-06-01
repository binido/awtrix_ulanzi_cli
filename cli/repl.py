from __future__ import annotations

import shlex
from argparse import ArgumentParser

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

from awtrix.client import AwtrixClient
from awtrix.config import CONFIG_PATH
from awtrix.i18n import I18n

_HISTORY_PATH = CONFIG_PATH.parent / ".awtrix_history"

_COMPLETER = NestedCompleter.from_nested_dict({
    "status": None,
    "power": {"on": None, "off": None},
    "reboot": None,
    "brightness": None,
    "settings": {"get": None, "set": None},
    "notify": None,
    "app": {"next": None, "prev": None, "list": None, "switch": None},
    "indicator": {"1": None, "2": None, "3": None},
    "help": None,
    "exit": None,
    "quit": None,
})

_STYLE = Style.from_dict({
    "prompt.ip":  "ansicyan bold",
    "prompt.sep": "ansibrightblack",
})


def _prompt(ip: str) -> FormattedText:
    return FormattedText([
        ("class:prompt.ip",  f"awtrix ({ip})"),
        ("class:prompt.sep", " > "),
    ])


def run_repl(ip: str, parser: ArgumentParser, i18n: I18n) -> None:
    print(i18n.t("repl_welcome"))
    print(i18n.t("repl_hint"))
    print()

    session: PromptSession = PromptSession(
        history=FileHistory(str(_HISTORY_PATH)),
        auto_suggest=AutoSuggestFromHistory(),
        completer=_COMPLETER,
        complete_while_typing=False,
        style=_STYLE,
    )

    with AwtrixClient(ip) as client:
        while True:
            try:
                raw = session.prompt(lambda: _prompt(ip))
            except KeyboardInterrupt:
                continue
            except EOFError:
                print()
                break

            line = raw.strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit"):
                break

            try:
                tokens = shlex.split(line)
            except ValueError as exc:
                print(i18n.t("repl_parse_error", error=exc))
                continue

            # Special: help [command] → forward to argparse --help
            if tokens[0] == "help":
                target = tokens[1:] + ["--help"] if len(tokens) > 1 else []
                try:
                    parser.parse_args(target or ["--help"])
                except SystemExit:
                    pass
                continue

            if tokens[0] in ("init", "shell"):
                print(i18n.t("repl_no_init") if tokens[0] == "init" else i18n.t("repl_already_in_shell"))
                continue

            try:
                args = parser.parse_args(tokens)
            except SystemExit:
                continue

            func = getattr(args, "func", None)
            if func is None:
                parser.print_help()
                continue

            func(args, client, i18n)
