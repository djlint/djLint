---
title: "Mustache Şablonları için Linter ve Biçimlendirici"
description: "djLint hem bir mustache şablon linter'ı hem de bir mustache şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın."
sidebar:
  label: "Mustache"
---

djLint hem bir mustache şablon linter'ı hem de bir mustache şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın.

**[Mustache nedir?](https://mustache.github.io/mustache.5.html)**

#### Komut satırını kullanma

```bash
djlint /path/to/templates --profile=handlebars
```

#### Ya da bir yapılandırma dosyası kullanın

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
