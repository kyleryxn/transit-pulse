#!/usr/bin/env python3
"""
Bump version across the repo.

- Reads the current version from version.txt (repo root). If missing, falls back to backend/api/main.py.
- Supports:
    * bump_version.py patch
    * bump_version.py minor
    * bump_version.py major
    * bump_version.py 1.2.3  (explicit)
- Updates:
    * version.txt
    * backend/api/main.py  (FastAPI(..., version="X.Y.Z", ...))

Optional:
    --dry-run  Show what would change without writing files.
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = REPO_ROOT / "version.txt"
MAIN_FILE = REPO_ROOT / "backend" / "api" / "main.py"

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$")

# Regex to find FastAPI version kwarg in main.py (handles newlines/spaces)
FASTAPI_VERSION_PATTERN = re.compile(
    r'(app\s*=\s*FastAPI\([^)]*?version\s*=\s*")[^"]+(")',
    re.DOTALL,
)

def parse_semver(s: str) -> Tuple[int, int, int, str | None]:
    m = SEMVER_RE.match(s.strip())
    if not m:
        raise ValueError(f"Invalid semver: {s!r}. Expected MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH-prerelease")
    major, minor, patch = map(int, m.groups()[:3])
    pre = m.group(4)  # optional prerelease
    return major, minor, patch, pre

def format_semver(major: int, minor: int, patch: int, pre: str | None = None) -> str:
    return f"{major}.{minor}.{patch}" + (f"-{pre}" if pre else "")

def read_current_version() -> str:
    # Prefer version.txt
    if VERSION_FILE.exists():
        v = VERSION_FILE.read_text(encoding="utf-8").strip()
        parse_semver(v)  # validate
        return v
    # Fallback: extract from main.py
    content = MAIN_FILE.read_text(encoding="utf-8")
    m = FASTAPI_VERSION_PATTERN.search(content)
    if not m:
        raise RuntimeError("Could not find FastAPI version in main.py and version.txt is missing.")
    return m.group(0).split('version=')[1].split('"')[1]

def bump_from_current(current: str, part: str) -> str:
    major, minor, patch, _pre = parse_semver(current)
    if part == "patch":
        patch += 1
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError("part must be one of: major, minor, patch")
    return format_semver(major, minor, patch)

def write_version_files(new_version: str, dry_run: bool = False) -> None:
    # Update version.txt
    if dry_run:
        print(f"[dry-run] Would write {VERSION_FILE} -> {new_version}")
    else:
        VERSION_FILE.write_text(new_version + "\n", encoding="utf-8")
        print(f"Updated {VERSION_FILE} -> {new_version}")

    # Update backend/api/main.py
    content = MAIN_FILE.read_text(encoding="utf-8")
    new_content, count = FASTAPI_VERSION_PATTERN.subn(rf'\g<1>{new_version}\2', content)
    if count == 0:
        raise RuntimeError("Could not locate FastAPI(..., version=\"...\") in main.py")
    if dry_run:
        print(f"[dry-run] Would update FastAPI version inside {MAIN_FILE}")
    else:
        MAIN_FILE.write_text(new_content, encoding="utf-8")
        print(f"Updated FastAPI version in {MAIN_FILE} -> {new_version}")

def main():
    parser = argparse.ArgumentParser(description="Bump or set repo version.")
    parser.add_argument("target", help="major | minor | patch | X.Y.Z")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing files")
    args = parser.parse_args()

    current = read_current_version()
    # Determine new version
    if args.target in {"major", "minor", "patch"}:
        new_version = bump_from_current(current, args.target)
    else:
        # explicit semver provided
        parse_semver(args.target)  # validate
        new_version = args.target.strip()

    print(f"Current version: {current}")
    print(f"New version:     {new_version}")
    write_version_files(new_version, dry_run=args.dry_run)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
