---
title: "Tera Şablonları için Linter ve Biçimlendirici"
description: "djLint, Tera şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için tera profilini ayarlayın."
sidebar:
  label: "Tera"
---

djLint, Tera şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `tera` profilini ayarlayın.

**[Tera nedir?](https://keats.github.io/tera/)**

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=tera
```

## Yapılandırma dosyasında

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
