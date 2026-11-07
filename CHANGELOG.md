# Değişiklik günlüğü

## [0.1.0] — 2026-11-07

İlk deneysel Türkçe topluluk sürümü. Temel: ShyFox 3.8.1.

### Düzeltmeler

- Firefox 156+ pencere algılayıcıları `popup-window` ve `chromehidden~="toolbar"` ile güncellendi ([PR #250](https://github.com/Naezr/ShyFox/pull/250)).
- `#navigator-toolbox` katman önceliği iyileştirildi ([PR #243](https://github.com/Naezr/ShyFox/pull/243)).
- Bul çubuğu yatay merkezleme kuralı güncellendi ([PR #243](https://github.com/Naezr/ShyFox/pull/243)).

### Proje altyapısı

- Türkçe README, kurulum ve sorun giderme rehberi.
- Dosya bazlı güvenli kurulum, yedek ve geri alma araçları (Python stdlib).
- CSS kaynak/kurulum birim testleri ve GitHub Actions.
- Hata/katkı şablonları ve orijinal geliştirici atıfları.

### Bilinen sınırlama

Firefox 159.0.1 üzerinde canlı GUI doğrulaması henüz yapılmadı. `0.1.0` kararlı sürüm iddiası taşımaz.
