---
title: Nunjucks Şablonları için Linter ve Biçimlendirici
keywords: nunjucks, djlint, nunjucks şablon linter'ı, nunjucks şablon biçimlendiricisi, nunjucks şablonlarını biçimlendirme, pebble, pebble şablon linter'ı
description: djLint, Nunjucks şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için nunjucks profilini ayarlayın.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Nunjucks nedir?](https://mozilla.github.io/nunjucks/)**

Pebble (Java) şablonları Twig ile uyumludur; bu yüzden onlar için de aynı profili kullanın.

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
