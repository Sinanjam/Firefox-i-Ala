#!/usr/bin/env python3
"""Surgically patch a ShyFox 3.8.1 profile for Firefox 156-159 (no Firefox profile reset).

Sources: Naezr/ShyFox PR #250 (chromehidden -> popup-window), #243 (toolbox stacking, findbar).
This is a best-effort community patch, not upstream and not a live Firefox 159 UI test.
"""
from __future__ import annotations
import argparse
import datetime
import pathlib
import re
import shutil
import subprocess
import sys

FILES = ["shy-global.css", "shy-navbar.css", "shy-sidebar.css", "shy-toolbar.css", "shy-findbar.css"]
TOOLBOX_OLD = """#navigator-toolbox {
  margin-top: -1px !important;
  position: relative;
  z-index: 3;
}"""
TOOLBOX_NEW = """#navigator-toolbox {
  margin-top: -1px !important;
  position: relative !important;
  z-index: 3 !important;
}"""
FINDBAR_OLD = """  left: calc(
    (
      100vw
      - var(--findbar-wdt)
      - var(--left-margin)
      - var(--right-margin)
    ) / 2
  );"""
FINDBAR_NEW = """  left: 50% !important;
  transform: translateX(-50%) !important;"""


def patch_css(name: str, css: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    if name != "shy-findbar.css":
        old_popup = ':not([chromehidden=""])'
        old_normal = '[chromehidden=""]'
        n = css.count(old_popup)
        if n:
            css = css.replace(old_popup, '[popup-window], [chromehidden~="toolbar"]')
            changes.append(f"Popup-window tespiti: {n}")
        n = css.count(old_normal)
        if n:
            css = css.replace(old_normal, ':not([popup-window], [chromehidden~="toolbar"])')
            changes.append(f"Normal pencere tespiti: {n}")
    if name == "shy-global.css" and TOOLBOX_OLD in css:
        css = css.replace(TOOLBOX_OLD, TOOLBOX_NEW, 1)
        changes.append("PR #243: navigator-toolbox z-index")
    if name == "shy-findbar.css" and FINDBAR_OLD in css:
        css = css.replace(FINDBAR_OLD, FINDBAR_NEW, 1)
        changes.append("PR #243: findbar ortalama")
    return css, changes


def main() -> int:
    ap = argparse.ArgumentParser(description="Firefox 159 uyumluluk yamasi: ShyFox gorunumunu korur.")
    ap.add_argument("--profile", required=True, help="Firefox profilinin yolu (about:profiles -> Root Directory)")
    ap.add_argument("--dry-run", action="store_true", help="Degisiklik yapmadan inceler")
    args = ap.parse_args()
    profile = pathlib.Path(args.profile).expanduser().resolve()
    css_root = profile / "chrome" / "ShyFox"
    if not css_root.is_dir() or not (profile / "chrome" / "userChrome.css").is_file():
        print(f"HATA: Burada ShyFox kurulumu bulunamadi: {css_root}", file=sys.stderr)
        return 2
    if not args.dry_run and shutil.which("pgrep"):
        for proc in ("firefox", "firefox-bin"):
            if subprocess.run(["pgrep", "-x", proc], stdout=subprocess.DEVNULL).returncode == 0:
                print("HATA: Önce Firefox'u tamamen kapat. Sonra scripti tekrar calistir.", file=sys.stderr)
                return 3
    pending: list[tuple[pathlib.Path, str, list[str]]] = []
    for name in FILES:
        path = css_root / name
        if not path.is_file():
            print(f"HATA: Beklenen ShyFox dosyasi eksik: {path}", file=sys.stderr)
            return 2
        old = path.read_text(encoding="utf-8")
        new, changes = patch_css(name, old)
        if name != "shy-findbar.css" and '[chromehidden=""]' in new:
            print(f"HATA: Tam yamalanmamis selector kaldi: {name}", file=sys.stderr)
            return 2
        if old != new:
            pending.append((path, new, changes))
            print(f"DEGISECEK: {name}: {', '.join(changes)}")
        else:
            print(f"ZATEN GUNCEL veya farkli: {name}")
    if not pending:
        print("Bu yamalar icin gerekli degisiklik kalmadi.")
        return 0
    if args.dry_run:
        print("Dry-run: profil dosyalarina dokunulmadi.")
        return 0
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = profile / "chrome" / ".shyfox-yedekler" / timestamp
    backup.mkdir(parents=True, exist_ok=False)
    try:
        for path, _, _ in pending:
            shutil.copy2(path, backup / path.name)
        for path, new, _ in pending:
            path.write_text(new, encoding="utf-8")
    except Exception:
        for path, _, _ in pending:
            old = backup / path.name
            if old.exists():
                shutil.copy2(old, path)
        raise
    print(f"YAMALAR UYGULANDI. Degisen {len(pending)} CSS yedeklendi: {backup}")
    print("Firefox'u acip Sidebery, navbar, toolbar ve Ctrl+L'yi kontrol et.")
    print("Geri almak icin: yedekteki CSS dosyalarini chrome/ShyFox/ icine kopyala.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
