#!/usr/bin/env python3
"""Firefox-ı Âlâ full theme installer. No Firefox profile reset.

All overwritten files are backed up, new files listed in a manifest.
Does not overwrite the user's existing user.js (even if opted in).
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKUPS = Path("chrome/.firefox-i-ala-backups")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def is_firefox_running() -> bool:
    if not shutil.which("pgrep"):
        return False
    return any(
        subprocess.run(
            ["pgrep", "-x", name], stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, check=False
        ).returncode == 0
        for name in ("firefox", "firefox-bin", "firefox-developer-edition")
    )


def atomic_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=dst.parent, prefix=".fia-", delete=False) as temp:
        temp_name = Path(temp.name)
        try:
            with src.open("rb") as infile:
                shutil.copyfileobj(infile, temp)
            temp.flush()
            os.fsync(temp.fileno())
        except BaseException:
            temp_name.unlink(missing_ok=True)
            raise
    try:
        os.replace(temp_name, dst)
    finally:
        temp_name.unlink(missing_ok=True)


def install(profile: Path, *, dry_run: bool = False,
            include_user_js: bool = False, check_process: bool = True) -> tuple[int, Path | None]:
    profile = profile.expanduser().resolve()
    if not profile.is_dir() or not (profile / "prefs.js").is_file():
        raise ValueError(f"Firefox profili geçersiz (prefs.js bulunamadı): {profile}")
    source_chrome = PROJECT_ROOT / "chrome"
    if not (source_chrome / "userChrome.css").is_file():
        raise ValueError("Paketin chrome/userChrome.css dosyası eksik")
    if not dry_run and check_process and is_firefox_running():
        raise RuntimeError("Firefox çalışıyor: kuruluma geçmeden önce tamamen kapat")

    sources = [(p, Path("chrome") / p.relative_to(source_chrome))
               for p in source_chrome.rglob("*") if p.is_file()]
    if include_user_js:
        sources.append((PROJECT_ROOT / "user.js", Path("user.js")))
    plan = []
    for source, relative in sorted(sources, key=lambda entry: str(entry[1])):
        dest = profile / relative
        if source.is_symlink() or dest.is_symlink():
            raise ValueError(f"Simgesel bağlantı desteklenmez: {relative}")
        if relative == Path("user.js") and dest.exists():
            print("ATLANDI: kullanıcıya ait user.js korunuyor")
            continue
        if dest.exists() and not dest.is_file():
            raise ValueError(f"Hedef dosya değil: {dest}")
        before = digest(dest) if dest.exists() else None
        after = digest(source)
        if before == after:
            continue
        status = "güncellenecek" if before else "eklenecek"
        print(f"{status.upper()}: {relative}")
        plan.append({"source": source, "relative": relative, "before": before, "after": after})
    if not plan:
        print("Değişiklik gerekmiyor; kurulum zaten güncel.")
        return 0, None
    print(f"Toplam {len(plan)} dosya değişecek.")
    if dry_run:
        print("Dry-run: Firefox profiline hiçbir dosya yazılmadı.")
        return len(plan), None

    backup_root = profile / BACKUPS / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_root.mkdir(parents=True, exist_ok=False)
    entries = []
    try:
        for part in plan:
            relative = part["relative"]
            dest = profile / relative
            if part["before"] is not None:
                saved = backup_root / "files" / relative
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dest, saved)
                if digest(saved) != part["before"]:
                    raise RuntimeError(f"Yedek doğrulanamadı: {relative}")
            entries.append({
                "path": relative.as_posix(),
                "before_sha256": part["before"],
                "after_sha256": part["after"],
            })
        (backup_root / "manifest.json").write_text(
            json.dumps({"format_version": 1, "project": "Firefox-i-Ala",
                        "files": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        for part in plan:
            destination = profile / part["relative"]
            atomic_copy(part["source"], destination)
            if digest(destination) != part["after"]:
                raise RuntimeError(f"Kopyalanan dosya doğrulanamadı: {part['relative']}")
    except Exception:
        print(f"HATA: işlem kesildi. Geri alma manifesti: {backup_root}", file=sys.stderr)
        raise
    print(f"KURULDU: {len(plan)} dosya. Geri alma yedeği: {backup_root}")
    print("Firefox ayarlarını ve Sidebery içe aktarmasını README'den tamamlayın.")
    return len(plan), backup_root


def main() -> int:
    p = argparse.ArgumentParser(description="Firefox-ı Âlâ güvenli tam tema kurulumu")
    p.add_argument("--profile", required=True, type=Path, help="about:profiles → Root Directory")
    p.add_argument("--dry-run", action="store_true", help="Yalnızca olası değişiklikleri göster")
    p.add_argument("--include-user-js", action="store_true", help="user.js yalnızca yoksa ekle")
    args = p.parse_args()
    try:
        install(args.profile, dry_run=args.dry_run, include_user_js=args.include_user_js)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"HATA: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
