---
title: "Linter i formater szablonów Django"
description: "djLint lintuje i formatuje szablony Django. Ustaw profil django, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Django"
---

djLint lintuje i formatuje szablony Django. Ustaw profil `django`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=django
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

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
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
