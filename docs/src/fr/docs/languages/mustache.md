---
title: Linter et formateur de templates Mustache
keywords: mustache, djlint, linter de templates mustache, formateur de templates mustache, formater des templates mustache
description: djLint linte et formate les templates Mustache. Utilisez le profil handlebars pour adapter les règles et le formatage à ces templates.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Qu'est-ce que Mustache ?](https://mustache.github.io/mustache.5.html)**

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
