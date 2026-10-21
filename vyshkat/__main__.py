"""Точка входа: python -m vyshkat [--demo]"""

import sys

from vyshkat.console import ConsoleApp
from vyshkat.container import build_container


def main() -> None:
    app = build_container().resolve(ConsoleApp)
    if "--demo" in sys.argv:
        app.run_demo()
    else:
        app.run()


if __name__ == "__main__":
    main()
