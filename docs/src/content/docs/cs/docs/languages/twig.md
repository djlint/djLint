---
title: "Linter a formátovač šablon Twig"
description: "djLint je linter a formátovač šablon Twig! Při lintování a formátování šablon pomocí djLint využijte připravený profil."
sidebar:
  label: "Twig"
---

djLint je linter a formátovač šablon Twig! Při lintování a formátování šablon pomocí djLint využijte připravený profil.

**[Co je Twig?](https://twig.symfony.com/)**

Šablony Pebble (Java) jsou kompatibilní s Twigem, takže pro ně použijte stejný profil.

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

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
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
