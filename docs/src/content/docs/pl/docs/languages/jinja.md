---
title: "Linter i formater szablonów Jinja"
description: "djLint to linter i formater szablonów jinja! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint."
sidebar:
  label: "Jinja"
---

djLint to linter i formater szablonów jinja! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.

**[Czym jest Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Szablony MiniJinja są w pełni zgodne z Jinja2, więc używaj tego samego profilu `jinja`.

Szablony Jinjava od HubSpot również są w stylu jinja, więc używaj tego profilu także dla nich.

#### Z wiersza poleceń

```bash
djlint /path/to/templates --profile=jinja
```

#### Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
