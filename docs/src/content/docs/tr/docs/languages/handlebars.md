---
title: "Handlebars Şablonları için Linter ve Biçimlendirici"
description: "djLint, Handlebars şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için handlebars profilini ayarlayın."
sidebar:
  label: "Handlebars"
---

djLint, Handlebars şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `handlebars` profilini ayarlayın.

**[Handlebars nedir?](https://handlebarsjs.com/)**

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=handlebars
```

## Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
