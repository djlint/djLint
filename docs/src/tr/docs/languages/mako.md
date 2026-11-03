---
title: Mako Şablonları için Linter ve Biçimlendirici
keywords: mako, python, pyramid, open edx, djlint, mako şablon linter'ı, mako şablon biçimlendiricisi, mako şablonlarını biçimlendirme
description: djLint, Mako şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için mako profilini ayarlayın.
tool: mako
---

# {{ title }}

{{ description }}

**[Mako nedir?](https://www.makotemplates.org/)**

mako profilinde `% if x:` gibi bir kontrol satırı ve `##` yorumu her zaman kendi satırında kalır, öznitelikleri kontrol satırlarına bağlı olan bir etiket de onları yazıldığı gibi korur. Python blokları ile `<%doc>` ve `<%text>` içeriği değiştirilmez; `--format-js` veya `--format-css` ile Mako sözdizimi içeren bir script ya da style da olduğu gibi bırakılır. `% if` ile `% endif` arasındaki satırlar ve her biri kendi satırında duran bir `<%block>` ya da `<%def>` etiketi ile kapanış etiketi arasındaki satırlar, diğer bloklar gibi girintilenir. Bir `${}` ifadesindeki kod yazıldığı gibi kalır.

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Tüm seçenekler için yapılandırma kılavuzuna göz atın!</a></div>
</div>
