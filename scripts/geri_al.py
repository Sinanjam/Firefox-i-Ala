#!/usr/bin/env python3
"""Restore a Firefox-ı Âlâ full-install backup without touching user changes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from kur import atomic_copy, digest, is_firefox_running


def restore(profile: Path, backup: Path, *, dry_run: bool = False,
            check_process: bool = True) -> tuple[int, int]:
    profile = profile.expanduser().resolve()
    backup = backup.expanduser().resolve()
    if not (profile / "prefs.js").is_file():
        raise ValueError(f"Firefox profili geçersiz: {profile}")
    # The backup belongs to this profile and must be under the installer's backup directory.
    expected_parent = (profile / "chrome" / ".firefox-i-ala-backups").resolve()
    if backup.parent != expected_parent:
        raise ValueError("Yedek, belirtilen Firefox profiline ait yedek klasöründe değil")
    manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("format_version") != 1 or manifest.get("project") != "Firefox-i-Ala":
        raise ValueError("Geçersiz yedek manifesti")
    if not dry_run and check_process and is_firefox_running():
        raise RuntimeError("Firefox çalışıyor: geri almadan önce tamamen kapat")

    changes, conflicts = [], []
    for item in manifest["files"]:
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts or not (
            relative.parts[0] == "chrome" or relative == Path("user.js")
        ):
            raise ValueError(f"Güvensiz manifest yolu: {relative}")
        target = profile / relative
        original_hash = item["before_sha256"]
        installed_hash = item["after_sha256"]
        if target.is_symlink():
            conflicts.append(f"Simge bağlantısı: {relative}")
            continue
        current_hash = digest(target) if target.is_file() else None
        if current_hash == original_hash:
            continue  # Already restored or never written during partial install.
        if current_hash != installed_hash:
            conflicts.append(f"Kurulumdan sonra değiştirilmiş: {relative}")
            continue
        if original_hash is not None:
            saved = backup / "files" / relative
            if not saved.is_file() or saved.is_symlink() or digest(saved) != original_hash:
                conflicts.append(f"Yedek bulunamadı/doğrulanamadı: {relative}")
                continue
        changes.append((relative, original_hash))

    for relative, original_hash in changes:
        print(f"{'SİLİNECEK' if original_hash is None else 'GERİ ALINACAK'}: {relative}")
    for problem in conflicts:
        print(f"DOKUNULMADI: {problem}")
    if dry_run:
        print("Dry-run: herhangi bir değişiklik yapılmadı.")
        return len(changes), len(conflicts)
    for relative, original_hash in changes:
        target = profile / relative
        if original_hash is None:
            target.unlink()
        else:
            atomic_copy(backup / "files" / relative, target)
    print(f"Geri alındı: {len(changes)} dosya, korunarak atlanan: {len(conflicts)}")
    return len(changes), len(conflicts)


def main() -> int:
    p = argparse.ArgumentParser(description="Firefox-ı Âlâ kurulumunu güvenle geri al")
    p.add_argument("--profile", required=True, type=Path)
    p.add_argument("--backup", required=True, type=Path)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    try:
        _, conflicts = restore(args.profile, args.backup, dry_run=args.dry_run)
        return 2 if conflicts else 0
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print(f"HATA: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
