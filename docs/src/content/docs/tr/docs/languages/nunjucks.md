---
title: "Nunjucks Şablonları için Linter ve Biçimlendirici"
description: "djLint, Nunjucks şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için nunjucks profilini ayarlayın."
sidebar:
  label: "Nunjucks"
---

djLint, Nunjucks şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `nunjucks` profilini ayarlayın.

**[Nunjucks nedir?](https://mozilla.github.io/nunjucks/)**

Pebble (Java) şablonları Twig ile uyumludur; bu yüzden onlar için de aynı profili kullanın.

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=nunjucks
```

## Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
