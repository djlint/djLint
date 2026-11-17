---
title: "Askama Şablonları için Linter ve Biçimlendirici"
description: "djLint, Askama şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için askama profilini ayarlayın."
sidebar:
  label: "Askama"
---

djLint, Askama şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `askama` profilini ayarlayın.

**[Askama nedir?](https://askama.readthedocs.io/)**

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=askama
```

## Yapılandırma dosyasında

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```
