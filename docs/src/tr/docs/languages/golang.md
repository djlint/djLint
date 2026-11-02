---
title: Go Şablonları için Linter ve Biçimlendirici
keywords: go şablonları, golang, djlint, go şablon linter'ı, go şablon biçimlendiricisi, golang şablon linter'ı, golang şablon biçimlendiricisi, go şablonlarını biçimlendirme, hugo şablon linter'ı, helm şablon linter'ı
description: djLint, Go şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için golang profilini ayarlayın.
tool: golang
---

# {{ title }}

{{ description }}

**[Go şablonları nedir?](https://pkg.go.dev/text/template)**

Go şablonları (`text/template`, `html/template`) Hugo temalarının ve Helm chart'larının da temelini oluşturur; bu yüzden onlar için de aynı profili kullanın.

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
