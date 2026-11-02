---
title: Angular Şablonları için Linter
keywords: angular, djlint, angular şablon linter'ı, angular şablonlarını denetleme
description: djLint, Angular şablonlarını denetler. Kuralların bu şablonlara uyması için angular profilini ayarlayın.
tool: angular
---

# {{ title }}

{{ description }}

**[Angular nedir?](https://angular.io/guide/template-syntax)**

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
