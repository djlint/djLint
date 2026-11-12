---
title: "Liquid Şablonları için Linter ve Biçimlendirici"
description: "djLint, Liquid şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için liquid profilini ayarlayın."
sidebar:
  label: "Liquid"
---

djLint, Liquid şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `liquid` profilini ayarlayın.

**[Liquid nedir?](https://shopify.github.io/liquid/)**

Tek bir profil tüm Liquid lehçelerini kapsar: Shopify temaları, Jekyll, LiquidJS (Eleventy) ve Fluid (Orchard Core).

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=liquid
```

## Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
