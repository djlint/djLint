---
title: Jinja Şablonları için Linter ve Biçimlendirici
keywords: jinja, djlint, jinja şablon linter'ı, jinja şablon biçimlendiricisi, jinja şablonlarını biçimlendirme, minijinja, jinjava, minijinja şablon linter'ı, jinjava şablon linter'ı
description: djLint, Jinja şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için jinja profilini ayarlayın.
tool: jinja
---

# {{ title }}

{{ description }}

**[Jinja nedir?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja şablonları Jinja2 ile tamamen uyumludur; bu yüzden aynı `jinja` profilini kullanın.

HubSpot'un Jinjava şablonları da jinja tarzındadır; bu yüzden onlar için de bu profili kullanın.

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
