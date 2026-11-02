---
title: Tera Şablonları için Linter ve Biçimlendirici
keywords: tera, rust, zola, djlint, tera şablon linter'ı, tera şablon biçimlendiricisi, tera şablonlarını biçimlendirme
description: djLint, Tera şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için tera profilini ayarlayın.
tool: tera
---

# {{ title }}

{{ description }}

**[Tera nedir?](https://keats.github.io/tera/)**

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
