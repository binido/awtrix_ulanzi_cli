from __future__ import annotations

import argparse
import sys
from typing import NoReturn

from awtrix.i18n import I18n


def make_parser_class(i18n: I18n) -> type[argparse.ArgumentParser]:
    """Return an ArgumentParser subclass whose error() appends a localized example line."""

    class LocalizedParser(argparse.ArgumentParser):
        _example: str = ""

        def error(self, message: str) -> NoReturn:
            self.print_usage(sys.stderr)
            print(f"{self.prog}: error: {message}", file=sys.stderr)
            if self._example:
                print(i18n.t("arg_example", example=self._example), file=sys.stderr)
            sys.exit(2)

    return LocalizedParser
