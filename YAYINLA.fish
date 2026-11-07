#!/usr/bin/env fish
# Firefox-ı Âlâ -> GitHub. Çalıştırmak için: fish YAYINLA.fish
# Bu betik, GitHub hesabında HERKESE AÇIK bir depo oluşturup kaynakları yükler.

set -l repo Sinanjam/Firefox-i-Ala
set -l folder (status dirname)
cd "$folder"; or exit 1

if not command -sq gh
    echo 'GitHub CLI (gh) kurulu değil. Arch: sudo pacman -S github-cli'
    exit 1
end
if not command -sq git
    echo 'git kurulu değil. Arch: sudo pacman -S git'
    exit 1
end

gh auth status >/dev/null 2>&1
if test $status -ne 0
    echo 'GitHub girişini yap: gh auth login'
    exit 1
end

set -l current_user (gh api user --jq .login 2>/dev/null)
if test "$current_user" != Sinanjam
    echo "Bağlı hesap $current_user; beklenen hesap Sinanjam. Yanlış hesaba yayınlanmıyor."
    exit 1
end

if not test -d .git
    git init -b main; or exit 1
end
set -l git_user (git config user.name)
if test -z "$git_user"
    echo 'Git kimliğin eksik: git config --global user.name "İsmin"'
    exit 1
end
set -l git_email (git config user.email)
if test -z "$git_email"
    echo 'Git e-posta ayarın eksik: git config --global user.email "GitHub noreply adresin"'
    exit 1
end

git add .; or exit 1
if not git diff --cached --quiet
    git commit -m 'feat: Firefox-ı Âlâ v0.1.0 Firefox 159 uyumluluk sürümü'; or exit 1
end

echo "GitHub üzerinde $repo herkese açık oluşturulacak ve main dalı yüklenecek."
read -l -P 'Devam edilsin mi? (EVET): ' confirm
if test "$confirm" != EVET
    echo 'İptal edildi.'
    exit 0
end

gh repo create "$repo" --public --source=. --remote=origin --push --description 'Firefox-ı Âlâ — ShyFox 3.8.1 tabanlı Firefox 159 uyumluluk düzeltmeleri ve Türkçe kurulum rehberi'
or exit 1

echo "Depo oluşturuldu: https://github.com/$repo"

# Kaynağı deneysel sürüm olarak yayımla; release başarısız olsa bile repo hazırdır.
if gh release create v0.1.0 -R "$repo" --target main --title 'Firefox-ı Âlâ v0.1.0 (Deneysel)' --notes-file CHANGELOG.md --prerelease
    echo "Sürüm sayfası: https://github.com/$repo/releases/tag/v0.1.0"
else
    echo "Depo yüklendi. İstersen sürümü daha sonra gh release create ile yayımlayabilirsin."
end
