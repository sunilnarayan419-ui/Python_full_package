"""Console-script entry point (`project.scripts.bioseqkit`), exposed
only when the optional `cli` extra (`click`) is installed.
"""
from __future__ import annotations

import sys

from .sequences import InvalidSequenceError, summarize
from .version import __version__


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args or args[0] in {"-h", "--help"}:
        print("usage: bioseqkit <SEQUENCE>")
        return 0
    if args[0] in {"-v", "--version"}:
        print(__version__)
        return 0
    try:
        stats = summarize(args[0])
    except InvalidSequenceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"length={stats.length} gc_content={stats.gc_content:.3f} counts={stats.base_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
