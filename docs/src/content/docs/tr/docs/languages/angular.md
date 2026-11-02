---
title: "Angular Şablonları için Linter"
description: "djLint bir Angular şablon linter'ıdır! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın."
sidebar:
  label: "Angular"
---

djLint bir Angular şablon linter'ıdır! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın.

**[Angular nedir?](https://angular.io/guide/template-syntax)**

#### Komut satırını kullanma

```bash
djlint /path/to/templates --profile=angular
```

#### Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile="angular"
```

```toml title="djlint.toml / .djlint.toml"
profile="angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
