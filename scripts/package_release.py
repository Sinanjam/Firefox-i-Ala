#!/usr/bin/env python3
"""Build a reproducible, installable Firefox-ı Âlâ release ZIP.

Only allowlisted user-facing files are shipped. The ZIP does not include
Git metadata, CI configuration, maintainer scripts, test fixtures or secrets.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "Firefox-i-Ala"
USER_FILES = (
    "README.md",
    "README.en.md",
    "CHANGELOG.md",
    "LICENSE",
    "sidebery-settings.json",
    "user.js",
)
USER_DIRECTORIES = ("chrome", "docs", "scripts")
EXCLUDED_PARTS = {".git", ".github", "__pycache__", ".DS_Store", ".pytest_cache"}
EXCLUDED_FILES = {"YAYINLA.fish", "package_release.py"}


def paths_to_ship() -> list[Path]:
    paths = [ROOT / name for name in USER_FILES]
    for d in USER_DIRECTORIES:
        directory = ROOT / d
        if not directory.is_dir():
            raise FileNotFoundError(f"Missing release directory: {directory}")
        paths.extend(p for p in directory.rglob("*") if p.is_file()
                     and not any(part in EXCLUDED_PARTS for part in p.relative_to(ROOT).parts)
                     and p.name not in EXCLUDED_FILES)
    for p in paths:
        if not p.is_file() or p.is_symlink():
            raise ValueError(f"Missing or unsafe release file: {p}")
    return sorted(paths, key=lambda p: p.relative_to(ROOT).as_posix())


def package_release(version: str, output: Path) -> tuple[Path, Path, int]:
    if not re.fullmatch(r"v\d+\.\d+\.\d+", version):
        raise ValueError("Version must be vX.Y.Z, e.g. v0.1.1")
    output.mkdir(parents=True, exist_ok=True)
    zip_path = output / "Firefox-i-Ala.zip"
    sum_path = output / "SHA256SUMS.txt"
    files = paths_to_ship()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9, strict_timestamps=True) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            entry = zipfile.ZipInfo(f"{PACKAGE_NAME}/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = (0o100644 << 16)
            archive.writestr(entry, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED,
                             compresslevel=9)
    checksum = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    sum_path.write_text(f"{checksum}  {zip_path.name}\n", encoding="utf-8")
    print(f"Created {zip_path} ({len(files)} files), checksum {sum_path}")
    return zip_path, sum_path, len(files)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Git tag, e.g. v0.1.1")
    parser.add_argument("--output", type=Path, default=Path("dist"))
    args = parser.parse_args()
    package_release(args.version, args.output)


if __name__ == "__main__":
    main()
