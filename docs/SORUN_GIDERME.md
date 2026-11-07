# Sorun giderme

## Tema hiç uygulanmıyor

- `about:profiles` ile gerçek profil yolunu doğrula.
- `about:config`: `toolkit.legacyUserProfileCustomizations.stylesheets = true`.
- `chrome/userChrome.css` ve `chrome/userContent.css` dosyaları var mı?
- Firefox'u tamamen kapatıp yeniden aç.

## Sol Sidebery paneli görünmüyor

- Sidebery eklentisinin kurulu/etkin ve Firefox'un kenar çubuğunda seçili olduğundan emin ol.
- `sidebar.revamp = false` ile eski kenar çubuğunu dene; Firefox sürümüne göre bu ayarın etkisi değişebilir.
- Sidebery ayarlarının yedeğini al, sonra `sidebery-settings.json` içe aktar.

## Adres çubuğuna yazı yazılmıyor

1. `Ctrl+L` ile odaklamayı dene.
2. `about:config` üzerinden `shyfox.disable.floating.search = true` ayarını **teşhis amacıyla** dene ve Firefox'u yeniden aç.
3. Yazılabiliyorsa sorun büyük olasılıkla yüzen arama düzeniyle ilgilidir. Bu ayarı geri `false` yaparak görünümü koruyabilirsin; issue açarken iki durumun ekran görüntüsünü paylaş.
4. Kullanıcı profilini sıfırlama veya Firefox'u standart temaya döndürme gerekli değildir.

## Sağ / üst araç çubuğu kayboldu

- Userchrome Toggle Extended ayarlarında "Allow multiple styles to be active together" ve ilk dört toggle etkin mi? "Apply changes" yapıldı mı?
- `shy-global.css`, `shy-navbar.css`, `shy-sidebar.css`, `shy-toolbar.css` içinde eski `chromehidden=""` kalmış mı?
- `scripts/fix_shyfox_159.py --profile "/profil/yolu" --dry-run` ile gerekli yama olup olmadığını kontrol et.

## Betik Firefox açık diyor

Firefox tüm pencerelerini kapat. Arka plandaki Firefox süreçlerini denetle (özellikle kurulum öncesinde). Verilerin güvenliği için açık profil üzerinde dosya değiştirilmez.

## Yedek veya işlem geri alma

Tam kurulum: `scripts/geri_al.py`; mevcut ShyFox onarımı: `chrome/.shyfox-yedekler/TARİH/`. Profilini silme.

## Hata bildirirken

Firefox sürümü, işletim sistemi, kurulum yöntemi, eklenti sürümleri ve ekran görüntüsü paylaş. **Profil klasörünün tamamını, `prefs.js` dosyasını, çerezleri, şifreleri, tokenları ya da oturum bilgilerini yükleme.**
