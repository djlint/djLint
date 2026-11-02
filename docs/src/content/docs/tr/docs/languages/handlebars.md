---
title: "Handlebars Şablonları için Linter ve Biçimlendirici"
description: "djLint hem bir handlebars şablon linter'ı hem de bir handlebars şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın."
sidebar:
  label: "Handlebars"
---

djLint hem bir handlebars şablon linter'ı hem de bir handlebars şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın.

**[Handlebars nedir?](https://handlebarsjs.com/)**

#### Komut satırını kullanma

```bash
djlint /path/to/templates --profile=handlebars
```

#### Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
