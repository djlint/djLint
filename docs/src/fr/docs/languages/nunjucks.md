---
title: Linter et formateur de templates Nunjucks
keywords: nunjucks, djlint, linter de templates nunjucks, formateur de templates nunjucks, formater des templates nunjucks, pebble, linter de templates pebble
description: djLint est un linter de templates nunjucks et un formateur de templates nunjucks ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Qu'est-ce que Nunjucks ?](https://mozilla.github.io/nunjucks/)**

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
