---
title: Liquid Template Linter and Formatter
keywords: liquid, shopify, jekyll, eleventy, djlint, liquid template linter, liquid template formatter, format liquid templates, shopify, jekyll, eleventy, liquidjs, fluid, shopify theme linter, jekyll linter
description: djLint est un linter de modèle Liquid et un formateur de modèle Liquid ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.
tool: liquid
---

# {{ title }}

{{ description }}

**[C'est quoi Liquid?](https://shopify.github.io/liquid/)**

Un seul profil couvre tous les dialectes Liquid : les thèmes Shopify, Jekyll, LiquidJS (Eleventy) et Fluid (Orchard Core).

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
