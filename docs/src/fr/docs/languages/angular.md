---
title: Linter de templates Angular
keywords: angular, djlint, linter de templates angular, linter des templates angular
description: djLint linte les templates Angular. Utilisez le profil angular pour adapter les règles à ces templates.
tool: angular
---

# {{ title }}

{{ description }}

**[Qu'est-ce qu'Angular ?](https://angular.io/guide/template-syntax)**

## En ligne de commande

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consultez le guide de configuration pour découvrir toutes les options !</a></div>
</div>
