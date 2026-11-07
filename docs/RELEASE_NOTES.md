# 🦊 Firefox-ı Âlâ v0.1.1 — Kolay indirilebilir deneysel sürüm

**Türkçe** · [English below](#english)

ShyFox 3.8.1 tabanlı Firefox 159 uyumluluk paketinin **Git kullanmadan indirilebilir ZIP sürümü**. CSS düzeltmeleri v0.1.0 ile aynıdır. **Firefox 159.0.1 üzerinde canlı arayüz testi henüz tamamlanmadı.**

### Kurulum

1. Aşağıdaki **Assets / Varlıklar** alanından **`Firefox-i-Ala.zip`** dosyasını indirip aç. GitHub'ın otomatik sunduğu **Source code (zip)** yerine bunu seç.
2. Firefox'ta `about:profiles` sayfasından aktif profilinin **Kök Dizin / Root Directory** yolunu öğren ve Firefox'u tamamen kapat.
3. Arşivden çıkan `Firefox-i-Ala` klasöründe terminal aç. Arch / Fish için örnek (profil yolunu değiştir):

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/kur.py --profile "$profile" --dry-run
python3 scripts/kur.py --profile "$profile"
```

4. Firefox `about:config` içinde `toolkit.legacyUserProfileCustomizations.stylesheets = true` ve (varsa) `sidebar.revamp = false` değerlerini kontrol et. Sidebery ile Userchrome Toggle Extended yapılandırmasını [Türkçe README](https://github.com/Sinanjam/Firefox-i-Ala/blob/main/README.md) üzerinden tamamla.

**Zaten ShyFox kullanıyorsan:** Tam temayı değiştirmeden yalnızca ilgili CSS dosyalarını `python3 scripts/fix_shyfox_159.py --profile "$profile"` ile güncelleyebilirsin (Firefox kapalı olmalı).

**Bütünlük kontrolü:** `SHA256SUMS.txt` dosyasını ZIP'in bulunduğu klasöre indirip `sha256sum -c SHA256SUMS.txt` çalıştır. Kurulum değiştirdiği dosyaları önceden yedekler.

---

## English

**Firefox-ı Âlâ v0.1.1 — experimental downloadable installer ZIP.** This is a packaging update of the ShyFox 3.8.1-based compatibility fork for Firefox 159. CSS fixes are unchanged from v0.1.0. **End-to-end testing on Firefox 159.0.1 has not yet been completed.**

1. Download and extract **`Firefox-i-Ala.zip`** from **Assets** below, **not** GitHub's auto-generated **Source code (zip)**.
2. Open `about:profiles`, copy the active profile's **Root Directory**, and fully close Firefox.
3. Open a terminal in the extracted `Firefox-i-Ala` folder. Example for Arch / Fish (replace the profile path):

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/kur.py --profile "$profile" --dry-run
python3 scripts/kur.py --profile "$profile"
```

4. In `about:config`, check `toolkit.legacyUserProfileCustomizations.stylesheets = true` and, if available, `sidebar.revamp = false`. Finish configuring Sidebery and Userchrome Toggle Extended via the [English README](https://github.com/Sinanjam/Firefox-i-Ala/blob/main/README.en.md).

If you're already using ShyFox, apply only the CSS updates with `python3 scripts/fix_shyfox_159.py --profile "$profile"` while Firefox is closed.

For checksum verification, place `SHA256SUMS.txt` next to the ZIP and run `sha256sum -c SHA256SUMS.txt`.

**Attribution:** Original ShyFox code by Naezr and contributors under MPL-2.0. Fork-specific patches and documentation were prepared via AI-assisted vibe coding.
