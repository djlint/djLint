---
title: "Linter a formátovač šablon Django"
description: "djLint je linter a formátovač šablon Django! Při lintování a formátování šablon pomocí djLint využijte připravený profil."
sidebar:
  label: "Django"
---

djLint je linter a formátovač šablon Django! Při lintování a formátování šablon pomocí djLint využijte připravený profil.

**[Co je Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile=django
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
