---
title: Linter et formateur de templates Liquid
keywords: liquid, shopify, jekyll, eleventy, djlint, linter de templates liquid, formateur de templates liquid, formater des templates liquid, shopify, jekyll, eleventy, liquidjs, fluid, linter de thèmes shopify, linter jekyll
description: djLint linte et formate les templates Liquid. Utilisez le profil liquid pour adapter les règles et le formatage à ces templates.
tool: liquid
---

# {{ title }}

{{ description }}

**[Qu'est-ce que Liquid ?](https://shopify.github.io/liquid/)**

Un seul profil couvre tous les dialectes de Liquid : thèmes Shopify, Jekyll, LiquidJS (Eleventy) et Fluid (Orchard Core).

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
