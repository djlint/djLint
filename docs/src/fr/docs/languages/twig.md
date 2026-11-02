---
title: Linter et formateur de templates Twig
keywords: twig, djlint, linter de templates twig, formateur de templates twig, formater des templates twig, pebble, linter de templates pebble
description: djLint est un linter de templates twig et un formateur de templates twig ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Qu'est-ce que Twig ?](https://twig.symfony.com/)**

Les templates Pebble (Java) sont compatibles avec Twig : utilisez ce même profil pour eux.

#### En ligne de commande

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consultez le guide de configuration pour découvrir toutes les options !</a></div>
</div>
