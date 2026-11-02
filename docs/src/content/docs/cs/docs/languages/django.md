---
title: "Linter a formátovač šablon Django"
description: "djLint lintuje a formátuje šablony Django. Nastavte profil django, aby jim pravidla i formátování odpovídaly."
sidebar:
  label: "Django"
---

djLint lintuje a formátuje šablony Django. Nastavte profil `django`, aby jim pravidla i formátování odpovídaly.

**[Co je Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Z příkazového řádku

```bash
djlint /path/to/templates --profile=django
```

## Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "django"
```

```toml title="djlint.toml / .djlint.toml"
profile = "django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
