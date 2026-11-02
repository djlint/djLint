---
title: Liquid Şablonları için Linter ve Biçimlendirici
keywords: liquid, shopify, jekyll, eleventy, djlint, liquid şablon linter'ı, liquid şablon biçimlendiricisi, liquid şablonlarını biçimlendirme, shopify, jekyll, eleventy, liquidjs, fluid, shopify tema linter'ı, jekyll linter'ı
description: djLint, Liquid şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için liquid profilini ayarlayın.
tool: liquid
---

# {{ title }}

{{ description }}

**[Liquid nedir?](https://shopify.github.io/liquid/)**

Tek bir profil tüm Liquid lehçelerini kapsar: Shopify temaları, Jekyll, LiquidJS (Eleventy) ve Fluid (Orchard Core).

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
