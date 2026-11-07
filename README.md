> [!IMPORTANT]
> **🤖 TAMAMEN VIBE CODING / AI ŞEFFAFLIĞI**
>
> **Firefox-ı Âlâ'nın ShyFox üzerine eklediği bütün uyumluluk yamaları, kurulum/geri alma betikleri, otomatik testler ve proje belgeleri, yapay zekâ (ChatGPT) ile yönlendirme temelli “vibe coding” yöntemi kullanılarak hazırlandı.** Projeyi yönlendiren kişi yazılımı satır satır elle geliştirdiğini veya bağımsız olarak denetlediğini iddia etmez. Otomatik testler, Firefox 159'da eksiksiz çalıştığı anlamına gelmez; canlı arayüz doğrulaması henüz yapılmadı.
>
> **Açıklama:** Orijinal [ShyFox](https://github.com/Naezr/ShyFox) teması ve önceki katkıcılarının çalışmaları bu iddianın **dışındadır**: özgün kod Naezr ve katkıcılarına aittir. Bu depo bağımsız, resmî olmayan bir türevdir.

# 🦊 Firefox-ı Âlâ

**ShyFox görünümünü sevenler için Firefox 159 uyumluluk çalışması.**

## 📦 Git clone yok — hazır sürümü indir

**[Firefox-ı Âlâ v0.1.1 — ZIP'i indir](https://github.com/Sinanjam/Firefox-i-Ala/releases/download/v0.1.1/Firefox-i-Ala.zip)** · [Tüm sürümler](https://github.com/Sinanjam/Firefox-i-Ala/releases) · [SHA-256 doğrulama](https://github.com/Sinanjam/Firefox-i-Ala/releases/download/v0.1.1/SHA256SUMS.txt)

İndirilen ZIP'i çıkar, Firefox'ta `about:profiles` üzerinden aktif profilinin kök yolunu bulup Firefox'u kapat. Arşivdeki `Firefox-i-Ala` klasöründe Fish terminalini aç:

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/kur.py --profile "$profile" --dry-run
python3 scripts/kur.py --profile "$profile"
```

**Profil yolunu kendi yolunla değiştir.** Eklenti/ayar adımları aşağıda. Git, GitHub CLI veya `git clone` gerekmez. ZIP'i mevcut ShyFox üzerine yamamak için `scripts/fix_shyfox_159.py` de paketin içindedir.



🌐 **Dil / Language:** 🇹🇷 Türkçe (bu sayfa) · [🇬🇧 English](README.en.md)

[![Doğrulama](https://github.com/Sinanjam/Firefox-i-Ala/actions/workflows/test.yml/badge.svg)](https://github.com/Sinanjam/Firefox-i-Ala/actions/workflows/test.yml)
![Lisans: MPL-2.0](https://img.shields.io/badge/lisans-MPL--2.0-blue)
![Hedef: Firefox 159](https://img.shields.io/badge/Firefox-159.0.1-orange)
![Durum: Deneysel](https://img.shields.io/badge/durum-deneysel-yellow)

> **Önemli:** Bu depo, [Naezr/ShyFox](https://github.com/Naezr/ShyFox) 3.8.1 tabanlı **bağımsız bir topluluk uyumluluk dalıdır**. Mozilla veya ShyFox geliştiricisinin resmî yayını değildir. CSS yamaları kaynak ve birim testleriyle kontrol edildi; **Firefox 159 üzerinde gerçek kullanıcı arayüzü testleri henüz tamamlanmadı.** Her özelliğin kusursuz çalıştığı ileri sürülmez.

## Nasıl görünüyor?

Orijinal ShyFox'un gizlenen araç çubukları, kenarlara yerleşen panelleri, Sidebery dikey sekmeleri ve yüzen adres çubuğu **korunur**. Orijinal geliştiricinin [görsel tanıtımına](https://github.com/Naezr/ShyFox#shy-on-surface-but-heavy-inside) bakabilirsiniz; bu depoya ait Firefox 159 ekran görüntüsü henüz yoktur.

## Neler düzeltildi? (v0.1.0)

| Bileşen | Yapılan işlem | Kaynak |
| --- | --- | --- |
| Firefox 156+ pencere algılama | Kaldırılan `chromehidden=""` seçicileri yerine `popup-window` ve `chromehidden~="toolbar"` kullanıldı | [ShyFox PR #250](https://github.com/Naezr/ShyFox/pull/250) |
| Üst araç kutusunun katmanı | `#navigator-toolbox` için `position` ve `z-index` değerlerine `!important` eklendi | [ShyFox PR #243](https://github.com/Naezr/ShyFox/pull/243) |
| Arama çubuğu (Ctrl+F) | Bul çubuğunun yatay merkezlenmesi güncellendi | [ShyFox PR #243](https://github.com/Naezr/ShyFox/pull/243) |

Yamalı dosyalar `chrome/ShyFox/` altında, tam tema ise `chrome/` klasöründedir. Kaynak: **ShyFox 3.8.1**. Hedef sürüm: Firefox **159.0.1** (3 Kasım 2026). Daha sonraki Firefox sürümleri için uyumluluk garanti edilmez.

## Gereksinimler

- Masaüstü **Mozilla Firefox** (159.0.1 hedef sürüm; diğer sürümler test edilmemiştir).
- [Sidebery](https://addons.mozilla.org/firefox/addon/sidebery/) (dikey sekmeler).
- [Userchrome Toggle Extended](https://github.com/Naezr/ShyFox#install) (panel görünürlüğü anahtarları; kurulum bağlantısı için orijinal rehberi izleyin).
- Firefox profilinde `toolkit.legacyUserProfileCustomizations.stylesheets = true`.
- Python **3.10+** (yalnızca kurulum, geri alma ve test betikleri için; temanın çalışması için gerekmez).
- **Arch Linux / Fish** örnekleri verilir; CSS diğer masaüstü işletim sistemlerinde de kullanılabilir ancak test edilmemiştir.

## Kurulum — mevcut ShyFox kullananlar

ShyFox zaten kuruluysa **önerilen yol budur**: kişisel simgeleri, eklentileri, Sidebery verilerini ve diğer profil dosyalarını değiştirmez; yalnızca beş CSS dosyasını yedekleyip yamalar.

1. Firefox'ta `about:profiles` sayfasından kullanılan profilin **Kök Dizin / Root Directory** yolunu bul.
2. Firefox'u tamamen kapat.
3. Fish terminalinde (klasör yolunu kendi profilinle değiştir):

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/fix_shyfox_159.py --profile "$profile" --dry-run
python3 scripts/fix_shyfox_159.py --profile "$profile"
```

Betik değiştirdiği dosyaları `chrome/.shyfox-yedekler/TARİH/` altında saklar. Dosyaları eski sürümle eşleşmiyorsa betik atlayabilir; bu durumda elle incele.

## Kurulum — ilk kez kuranlar veya tam temayı değiştirmek isteyenler

Bu depoyu ZIP olarak indirip açabilir veya klonlayabilirsin. **Mevcut Firefox profilini silme.**

```fish
set profile ~/.mozilla/firefox/xxxxxxxx.default-release
python3 scripts/kur.py --profile "$profile" --dry-run
python3 scripts/kur.py --profile "$profile"
```

Kurulum **yalnızca `chrome/` içindeki tema dosyalarını** kopyalar; farklı dosyaları silmez, üzerine yazılanları geri alma için yedekler. `user.js` **otomatik olarak değiştirilmez**. Yeni profilde istersen `--include-user-js` kullanabilirsin; varsa mevcut `user.js` hiçbir koşulda üzerine yazılmaz. Firefox kapalı olmalıdır.

Sonra `about:config` içinde `toolkit.legacyUserProfileCustomizations.stylesheets = true` ve klasik kenar çubuğu için `sidebar.revamp = false` ayarlarını kontrol et. Sidebery'ye `sidebery-settings.json` dosyasını **elle içe aktar** (var olan Sidebery ayarlarının üzerine yazabilir; önce dışa aktar). Userchrome Toggle Extended içinde **Allow multiple styles to be active together** seçeneğini ve ilk dört anahtarı etkinleştirip **Apply changes** yap. Tam adımlar: [Kurulum kılavuzu](docs/KURULUM.md).

## Geri alma

- **Tam kurulum:** Kurulumun yazdırdığı yedek klasörü ile `python3 scripts/geri_al.py --profile "$profile" --backup "/yedek/klasoru" --dry-run`, ardından `--dry-run` olmadan çalıştır. Sadece kurulumun bıraktığı hâliyle duran dosyaları geri alır; sonradan değişmiş dosyalara dokunmaz.
- **Beş CSS yaması:** `chrome/.shyfox-yedekler/TARİH/` klasöründeki dosyaları Firefox kapalıyken `chrome/ShyFox/` içine geri kopyala.

Firefox'u kaldırman, profilini sıfırlaman veya ShyFox'tan vazgeçmen gerekmez.

## Bilinen sorunlar

- Yüzen adres çubuğu yazı almıyorsa önce `Ctrl+L` ile test et. `about:config` → `shyfox.disable.floating.search = true` geçici teşhis için kullanılabilir; sadece bu görsel özelliği kapatır. Çözüm kanıtı değildir.
- Sidebery'nin görünmemesi CSS yerine eklenti seçimi ya da eski/yeni Firefox kenar çubuğu düzeninden kaynaklanabilir.
- Firefox güncellemeleri bu özel CSS'leri tekrar bozabilir.
- Firefox 159 üzerinde uçtan uca GUI testi henüz yapılmadı; bulgular ve ekran görüntüleri değerlidir.

[**Sorun giderme**](docs/SORUN_GIDERME.md) · [**Değişiklikler**](CHANGELOG.md)

## Telif ve teşekkür

Orijinal tasarım ve kaynak kod [Naezr/ShyFox](https://github.com/Naezr/ShyFox) geliştiricisine aittir; lisansı **Mozilla Public License 2.0**. [Orijinal README](docs/ORIJINAL_SHYFOX_README.md) ve `LICENSE` dosyası korunmuştur. İçerikte kullanılan simgeler ve duvar kâğıdı için orijinal projenin teşekkür/kaynak bölümüne bakın. PR #243 ve #250 katkıcılarına da teşekkürler.

**Firefox-ı Âlâ**, bu kaynağın Türkçe dokümantasyonlu, uyumluluk düzeltmeleri taşıyan bağımsız türevidir. Firefox ve ShyFox markalarının resmî ürünü değildir.
