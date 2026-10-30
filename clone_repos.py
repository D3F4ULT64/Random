#!/usr/bin/env python3
"""Clone all repositories for the authenticated GitHub user into MyRepos.

Requires Git and the GitHub CLI (gh), with `gh auth login` completed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

OWNER = "D3F4ULT64"
DESTINATION = Path("MyRepos")


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        text=True,
        capture_output=capture,
        check=False,
    )


def main() -> int:
    DESTINATION.mkdir(parents=True, exist_ok=True)

    # Use GitHub CLI so private repositories are included when the user is logged in.
    result = run(
        [
            "gh",
            "repo",
            "list",
            OWNER,
            "--limit",
            "1000",
            "--json",
            "name,url",
        ],
        capture=True,
    )

    if result.returncode != 0:
        print("Could not list GitHub repositories.")
        print(result.stderr.strip())
        print("Run `gh auth login` first, then try again.")
        return result.returncode or 1

    try:
        repos = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"Invalid GitHub CLI response: {exc}")
        return 1

    if not repos:
        print("No repositories found.")
        return 0

    print(f"Found {len(repos)} repositories. Cloning into {DESTINATION.resolve()}...\n")

    failed = 0
    for repo in repos:
        name = repo["name"]
        url = repo["url"]
        target = DESTINATION / name

        if target.exists():
            print(f"[SKIP] {name} already exists")
            continue

        print(f"[CLONE] {name}")
        result = run(["git", "clone", url, str(target)])

        if result.returncode == 0:
            print(f"[OK] {name}\n")
        else:
            failed += 1
            print(f"[FAILED] {name}\n")

    print(f"Finished. {len(repos) - failed} successful, {failed} failed/skipped.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
