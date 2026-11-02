---
title: "Twig Şablonları için Linter ve Biçimlendirici"
description: "djLint hem bir twig şablon linter'ı hem de bir twig şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın."
sidebar:
  label: "Twig"
---

djLint hem bir twig şablon linter'ı hem de bir twig şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın.

**[Twig nedir?](https://twig.symfony.com/)**

Pebble (Java) şablonları Twig ile uyumludur; bu yüzden onlar için de aynı profili kullanın.

#### Komut satırını kullanma

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile="nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile="nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
