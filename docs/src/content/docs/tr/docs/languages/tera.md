---
title: "Tera Şablonları için Linter ve Biçimlendirici"
description: "djLint hem bir Tera şablon linter'ı hem de bir Tera şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın."
sidebar:
  label: "Tera"
---

djLint hem bir Tera şablon linter'ı hem de bir Tera şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın.

**[Tera nedir?](https://keats.github.io/tera/)**

#### Komut satırını kullanma

```bash
djlint /path/to/templates --profile=tera
```

#### Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
