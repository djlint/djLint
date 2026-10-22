---
title: Angular Template Linter
keywords: angular, djlint, angular template linter, lint angular templates
description: djLint est un linter de templates Angular ! Profitez du profil pré-construit lorsque vous lintez et formatez vos templates avec djLint.
tool: angular
---

# {{ title }}

{{ description }}

**[C'est quoi Angular?](https://angular.io/guide/template-syntax)**

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>
