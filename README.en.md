> [!IMPORTANT]
> **🤖 100% VIBE CODING / AI TRANSPARENCY**
>
> **All Firefox-ı Âlâ additions on top of ShyFox—including compatibility patches, install/restore scripts, automated tests and project documentation—were prepared through AI-assisted “vibe coding” with ChatGPT.** The person directing the project does not claim to have hand-written or independently audited every line. Passing automated checks does not establish that the theme works flawlessly in Firefox 159; live GUI validation has not yet been completed.
>
> **Scope:** The original [ShyFox](https://github.com/Naezr/ShyFox) theme and previous contributors' work are **not** being claimed as AI-generated. Credit for that original code belongs to Naezr and its contributors. This is an independent, unofficial derivative.

# 🦊 Firefox-ı Âlâ

**A Firefox 159 compatibility effort for people who love the ShyFox look.**

## 📦 No Git clone — download a ready-to-install ZIP

**[Download Firefox-ı Âlâ v0.1.1 ZIP](https://github.com/Sinanjam/Firefox-i-Ala/releases/download/v0.1.1/Firefox-i-Ala.zip)** · [All releases](https://github.com/Sinanjam/Firefox-i-Ala/releases) · [SHA-256 checksum](https://github.com/Sinanjam/Firefox-i-Ala/releases/download/v0.1.1/SHA256SUMS.txt)

Extract the ZIP, locate your active Firefox profile's **Root Directory** at `about:profiles`, and close Firefox. Open a Fish terminal in the extracted `Firefox-i-Ala` directory:

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/kur.py --profile "$profile" --dry-run
python3 scripts/kur.py --profile "$profile"
```

**Replace the sample profile path with your real one.** Complete the extension/settings steps below. No Git, GitHub CLI or `git clone` required. The ZIP also includes `scripts/fix_shyfox_159.py` if you only want to patch an existing ShyFox setup.



🌐 **Language / Dil:** [🇹🇷 Türkçe](README.md) · 🇬🇧 English (this page)

[![Checks](https://github.com/Sinanjam/Firefox-i-Ala/actions/workflows/test.yml/badge.svg)](https://github.com/Sinanjam/Firefox-i-Ala/actions/workflows/test.yml)
![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue)
![Target: Firefox 159](https://img.shields.io/badge/Firefox-159.0.1-orange)
![Status: Experimental](https://img.shields.io/badge/status-experimental-yellow)

> **Important:** This repository is an **independent community compatibility fork** based on [Naezr/ShyFox](https://github.com/Naezr/ShyFox) 3.8.1. It is not an official release from Mozilla or the original ShyFox developer. CSS changes were checked against their sources and the included automated tests, but **the interface has not yet been tested end-to-end on Firefox 159**. Full functionality is not guaranteed.

## What does it look like?

The original ShyFox design is preserved: auto-hiding toolbars, edge-mounted panels, vertical tabs with Sidebery, and the floating address bar. See the [original ShyFox showcase](https://github.com/Naezr/ShyFox#shy-on-surface-but-heavy-inside); this fork does not yet have verified Firefox 159 screenshots.

## What's fixed? (v0.1.0)

| Component | Change | Source |
| --- | --- | --- |
| Firefox 156+ window detection | Replaced removed `chromehidden=""` selectors with `popup-window` and `chromehidden~="toolbar"` logic | [ShyFox PR #250](https://github.com/Naezr/ShyFox/pull/250) |
| Top toolbox stacking | Added `!important` to the `position` and `z-index` rules for `#navigator-toolbox` | [ShyFox PR #243](https://github.com/Naezr/ShyFox/pull/243) |
| Find bar (Ctrl+F) | Updated the find bar's horizontal centering | [ShyFox PR #243](https://github.com/Naezr/ShyFox/pull/243) |

Patched files live under `chrome/ShyFox/`; the full theme is in `chrome/`. Upstream baseline: **ShyFox 3.8.1**. Target: **Firefox 159.0.1** (November 3, 2026). Compatibility with subsequent Firefox versions is not guaranteed.

## Requirements

- Desktop **Mozilla Firefox** (target: 159.0.1; other versions have not been tested).
- [Sidebery](https://addons.mozilla.org/firefox/addon/sidebery/) for vertical tabs.
- [Userchrome Toggle Extended](https://github.com/Naezr/ShyFox#install) for panel visibility controls; see the original guide for its installation.
- Firefox preference `toolkit.legacyUserProfileCustomizations.stylesheets = true`.
- **Python 3.10+** for the included install, restore and test scripts; Python is **not** required for the theme itself.
- Commands below target **Arch Linux and Fish**. The CSS can be used on other desktop operating systems, but they have not been tested here.

## Installing over an existing ShyFox setup

**Recommended if you already use ShyFox.** This method preserves your extensions, Sidebery data and other Firefox profile files; it backs up and updates only five CSS files.

1. Open `about:profiles` in Firefox and find your active profile's **Root Directory**.
2. Close Firefox completely.
3. Run these commands in Fish, replacing the example path with your actual profile:

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/fix_shyfox_159.py --profile "$profile" --dry-run
python3 scripts/fix_shyfox_159.py --profile "$profile"
```

The patcher saves the original files in `chrome/.shyfox-yedekler/DATE/`. If your local CSS differs from the expected upstream version, the patcher may skip some files; review those manually.

## Fresh install or replacing the complete theme

Download and extract this repository, or clone it. **Do not delete your existing Firefox profile.**

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/kur.py --profile "$profile" --dry-run
python3 scripts/kur.py --profile "$profile"
```

Only theme files under `chrome/` are copied. Unrelated files are not deleted; overwritten theme files are backed up. `user.js` is **not** modified by default. You may opt in with `--include-user-js` for a new profile; an existing `user.js` will **never** be overwritten. Firefox must be closed while installing.

Then verify `toolkit.legacyUserProfileCustomizations.stylesheets = true` and `sidebar.revamp = false` in `about:config`. Import `sidebery-settings.json` **manually** in Sidebery (export your current settings first). In Userchrome Toggle Extended, enable **Allow multiple styles to be active together**, activate the first four toggles and select **Apply changes**. For detailed steps, see the [Turkish installation guide](docs/KURULUM.md).

## Rollback

- **Complete install:** Use the backup folder printed by the installer. Run `python3 scripts/geri_al.py --profile "$profile" --backup "/path/to/backup" --dry-run`, then repeat without `--dry-run`. The script restores only files that have not been changed again since installation.
- **Five CSS patches:** Close Firefox and copy the files from `chrome/.shyfox-yedekler/DATE/` back into `chrome/ShyFox/`.

You do **not** need to uninstall Firefox, reset your profile or abandon the ShyFox design.

## Known limitations

- If the floating address bar cannot accept input, try `Ctrl+L`. Temporarily setting `shyfox.disable.floating.search = true` in `about:config` may help isolate the issue; **this is a diagnostic step, not a verified fix**.
- Missing Sidebery may be caused by the selected sidebar extension or Firefox's classic versus revamped sidebar, rather than CSS.
- Future Firefox updates may break unsupported interface customizations again.
- No end-to-end GUI testing on Firefox 159 has been completed yet.

[**Troubleshooting (Turkish)**](docs/SORUN_GIDERME.md) · [**Changelog (Turkish)**](CHANGELOG.md)

## Copyright and credits

Original design and source code: [Naezr/ShyFox](https://github.com/Naezr/ShyFox), distributed under **Mozilla Public License 2.0**. The [original README](docs/ORIJINAL_SHYFOX_README.md) and `LICENSE` have been preserved. For third-party icons and wallpapers, see the original project's credits. Thank you to the contributors of upstream PRs #243 and #250.

**Firefox-ı Âlâ** is an independent derivative with Turkish documentation and compatibility patches. It is not an official Firefox, Mozilla or ShyFox product.
