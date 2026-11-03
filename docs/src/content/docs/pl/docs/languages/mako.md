---
title: "Linter i formater szablonów Mako"
description: "djLint lintuje i formatuje szablony Mako. Ustaw profil mako, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Mako"
---

djLint lintuje i formatuje szablony Mako. Ustaw profil `mako`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Mako?](https://www.makotemplates.org/)**

W profilu mako wiersz sterujący, taki jak `% if x:`, i komentarz `##` zawsze zajmują osobny wiersz, a tag, którego atrybuty zależą od wierszy sterujących, zachowuje je w zapisanej postaci. Bloki Pythona i zawartość `<%doc>` oraz `<%text>` zostają bez zmian, podobnie jak script lub style ze składnią Mako przy `--format-js` lub `--format-css`. Wiersze między `% if` a `% endif` oraz między tagiem `<%block>` lub `<%def>` a jego tagiem zamykającym, gdy każdy z nich stoi w osobnym wierszu, są wcinane jak każdy inny blok. Kod w wyrażeniu `${}` zostaje w zapisanej postaci.

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=mako
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
