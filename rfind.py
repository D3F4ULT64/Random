#!/usr/bin/env python3
"""Fast, dependency-free recursive file finder."""

from __future__ import annotations

import argparse
import fnmatch
import os
from pathlib import Path

DEFAULT_IGNORES = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv"}


def human_size(size: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{size} B"
        value /= 1024
    return f"{size} B"


def find_files(root: Path, pattern: str, ignored: set[str], min_size: int | None, max_size: int | None):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ignored and not d.startswith(".")]
        for name in files:
            if name.startswith(".") or not fnmatch.fnmatch(name, pattern):
                continue
            path = Path(current) / name
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if min_size is not None and size < min_size:
                continue
            if max_size is not None and size > max_size:
                continue
            yield path, size


def main() -> int:
    parser = argparse.ArgumentParser(description="Recursively find files without external dependencies.")
    parser.add_argument("pattern", nargs="?", default="*", help="Filename pattern, e.g. '*.py' or 'config.*'")
    parser.add_argument("path", nargs="?", default=".", help="Directory to search")
    parser.add_argument("--min-size", type=int, metavar="BYTES", help="Only show files at least this large")
    parser.add_argument("--max-size", type=int, metavar="BYTES", help="Only show files at most this large")
    parser.add_argument("--all", action="store_true", help="Also search hidden directories/files")
    parser.add_argument("--no-ignore", action="store_true", help="Do not skip common dependency/build directories")
    parser.add_argument("--stats", action="store_true", help="Print a summary after the results")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    ignored = set() if args.no_ignore else DEFAULT_IGNORES
    count = 0
    total = 0
    for path, size in find_files(root, args.pattern, ignored, args.min_size, args.max_size):
        count += 1
        total += size
        print(f"{path.relative_to(root)}\t{human_size(size)}")

    if args.stats:
        print(f"\n{count} file(s), {human_size(total)} total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
