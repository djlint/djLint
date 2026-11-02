---
title: "Linter i formater szablonów Django"
description: "djLint to linter i formater szablonów django! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint."
sidebar:
  label: "Django"
---

djLint to linter i formater szablonów django! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.

**[Czym jest Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Z wiersza poleceń

```bash
djlint /path/to/templates --profile=django
```

#### Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

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
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
