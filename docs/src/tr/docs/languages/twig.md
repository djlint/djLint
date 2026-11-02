---
title: Twig Şablonları için Linter ve Biçimlendirici
keywords: twig, djlint, twig şablon linter'ı, twig şablon biçimlendiricisi, twig şablonlarını biçimlendirme, pebble, pebble şablon linter'ı
description: djLint hem bir twig şablon linter'ı hem de bir twig şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Twig nedir?](https://twig.symfony.com/)**

Pebble (Java) şablonları Twig ile uyumludur; bu yüzden onlar için de aynı profili kullanın.

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
