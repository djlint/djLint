---
title: Mustache Şablonları için Linter ve Biçimlendirici
keywords: mustache, djlint, mustache şablon linter'ı, mustache şablon biçimlendiricisi, mustache şablonlarını biçimlendirme
description: djLint hem bir mustache şablon linter'ı hem de bir mustache şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Mustache nedir?](https://mustache.github.io/mustache.5.html)**

#### Komut satırını kullanma

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Tüm seçenekler için yapılandırma kılavuzuna göz atın!</a></div>
</div>
