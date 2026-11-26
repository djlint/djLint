---
title: "Angular Şablonları için Linter"
description: "djLint, Angular şablonlarını denetler. Kuralların bu şablonlara uyması için angular profilini ayarlayın."
sidebar:
  label: "Angular"
---

djLint, Angular şablonlarını denetler. Kuralların bu şablonlara uyması için `angular` profilini ayarlayın.

**[Angular nedir?](https://angular.dev/guide/templates)**

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=angular
```

## Yapılandırma dosyasında

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```
