# Kurulum rehberi (Arch Linux + Fish)

## 1) Firefox profilini seç

Firefox adres çubuğuna `about:profiles` yaz. Kullanılan profilin **Kök Dizin** yolunu kopyala. `~/.mozilla/firefox/xxxxxxxx.default-release` burada **örnek** yoldur; dağıtım, Flatpak veya başka profillerde değişebilir.

> **Önemli:** Firefox'u tamamen kapat. Birden fazla profil varsa yanlış profili seçmediğini kontrol et.

## 2) Mevcut ShyFox'u güncelle

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/fix_shyfox_159.py --profile "$profile" --dry-run
python3 scripts/fix_shyfox_159.py --profile "$profile"
```

Betik beş eski CSS dosyasını yerinde onarır. Var olan `chrome/userChrome.css`, `chrome/userContent.css`, `user.js`, Firefox verileri ve Sidebery eklenti verileri korunur. Değişen dosyaların yedeği `chrome/.shyfox-yedekler/` altında tutulur.

## 3) Yeni kurulum / tam kopyalama

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/kur.py --profile "$profile" --dry-run
python3 scripts/kur.py --profile "$profile"
```

`kur.py`, `chrome/` dosyaları için değişiklikten önce geri alınabilir manifestli yedek alır. Var olmayan dosyaları oluşturur; mevcut tema dosyalarını gerektiğinde günceller. `user.js` üzerine yazılmaz. `--include-user-js` yalnızca **yoksa** ekler; bazı Firefox tercihleri `user.js` tarafından her açılışta tekrar uygulanabileceğinden dikkatli kullan.

## 4) Eklenti ve ayarlar

1. `about:config` içinde `toolkit.legacyUserProfileCustomizations.stylesheets = true` yap.
2. Klasik Sidebery düzeni için `sidebar.revamp = false` ayarını dene. Bu ayarın geçerliliğini kendi sürümünde kontrol et.
3. [Sidebery](https://addons.mozilla.org/firefox/addon/sidebery/) yükle ve sol kenar çubuğunda seçili olduğuna emin ol.
4. Sidebery **Settings → Import** üzerinden `sidebery-settings.json` içe aktar. **Önce mevcut Sidebery ayarlarını dışa aktar.**
5. [ShyFox'un Userchrome Toggle Extended yönergelerini](https://github.com/Naezr/ShyFox#install) uygula: "Allow multiple styles to be active together" açık, ilk dört toggle açık, ardından "Apply changes".
6. Menü → Diğer araçlar → Araç çubuğunu özelleştir içinden simge konumlarını ShyFox düzenine göre yerleştir. Sonra Firefox'u yeniden başlat.

## 5) Kontrol listesi

- `Ctrl+L`: adres satırına yazı giriliyor mu?
- `Ctrl+F`: arama alanı ortalanıyor mu?
- Sidebery sekmeleri ve soldaki panel açılıp kapanıyor mu?
- Sağ dikey araç çubuğu ve üst araç çubuğu erişilebilir mi?
- Yeni sekme görüntüsü ve karanlık/açık tema doğru mu?
- Tam ekran (`F11`) ve açılır kimlik doğrulama pencerelerinde arayüz düzgün mü?

Test sonuçlarını issue olarak paylaşmak için [hata bildirim şablonunu](../.github/ISSUE_TEMPLATE/bug_report.yml) kullan.

## Geri alma

Tam kurulumun sonunda gösterilen yedek klasörünü kaydet. Firefox kapalıyken:

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/geri_al.py --profile "$profile" --backup "/yedek/klasoru" --dry-run
python3 scripts/geri_al.py --profile "$profile" --backup "/yedek/klasoru"
```

Dosyalarda kurulumdan sonra değişiklik yapılmışsa geri alma bunları atlar. **Yanlış veya eski yedeği rastgele kullanma**.
