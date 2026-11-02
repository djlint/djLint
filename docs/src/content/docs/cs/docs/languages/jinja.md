---
title: "Linter a formátovač šablon Jinja"
description: "djLint je linter a formátovač šablon Jinja! Při lintování a formátování šablon pomocí djLint využijte připravený profil."
sidebar:
  label: "Jinja"
---

djLint je linter a formátovač šablon Jinja! Při lintování a formátování šablon pomocí djLint využijte připravený profil.

**[Co je Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Šablony MiniJinja jsou plně kompatibilní s Jinja2, takže použijte stejný profil `jinja`.

Šablony Jinjava od HubSpotu jsou také ve stylu jinja, takže pro ně použijte tento profil také.

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile=jinja
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile="jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile="jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
