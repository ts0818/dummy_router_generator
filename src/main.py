"""
Entry point for the router generator CLI.

Usage:
    python -m src.main input.csv
"""

import sys
from typing import Sequence

from src.app.router_app import RouterApp

def main(argv: Sequence[str] | None = None) -> None:
    """
    Parse CLI arguments and invoke RouterApp.

    Args:
        argv: Sequence of arguments (defaults to sys.argv if None).

    Returns:
        None
    """
    args: Sequence[str] = argv if argv is not None else sys.argv

    if len(args) < 2:
        print("Usage: python -m src.main input.csv")
        return

    csv_file: str = args[1]

    try:
        app = RouterApp(csv_file)
        app.run()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
