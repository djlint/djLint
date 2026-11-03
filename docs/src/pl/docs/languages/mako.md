---
title: Linter i formater szablonów Mako
keywords: mako, python, pyramid, open edx, djlint, linter szablonów mako, formater szablonów mako, formatowanie szablonów mako
description: djLint lintuje i formatuje szablony Mako. Ustaw profil mako, aby reguły i formatowanie były do nich dopasowane.
tool: mako
---

# {{ title }}

{{ description }}

**[Czym jest Mako?](https://www.makotemplates.org/)**

W profilu mako wiersz sterujący, taki jak `% if x:`, i komentarz `##` zawsze zajmują osobny wiersz, a tag, którego atrybuty zależą od wierszy sterujących, zachowuje je w zapisanej postaci. Bloki Pythona i zawartość `<%doc>` oraz `<%text>` zostają bez zmian, podobnie jak script lub style ze składnią Mako przy `--format-js` lub `--format-css`. Wiersze sterujące nie wcinają jeszcze swojej zawartości.

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Wszystkie opcje znajdziesz w przewodniku po konfiguracji!</a></div>
</div>
