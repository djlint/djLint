---
title: Linter et formateur de templates Mako
keywords: mako, python, pyramid, open edx, djlint, linter de templates mako, formateur de templates mako, formater des templates mako
description: djLint linte et formate les templates Mako. Utilisez le profil mako pour adapter les règles et le formatage à ces templates.
tool: mako
---

# {{ title }}

{{ description }}

**[Qu'est-ce que Mako ?](https://www.makotemplates.org/)**

Avec le profil mako, une ligne de contrôle comme `% if x:` et un commentaire `##` gardent toujours une ligne à eux, et une balise dont les attributs dépendent de lignes de contrôle les garde tels qu'ils sont écrits. Les blocs Python et le contenu de `<%doc>` et `<%text>` ne sont pas modifiés, pas plus qu'un script ou un style qui contient de la syntaxe Mako avec `--format-js` ou `--format-css`. Les lignes de contrôle n'indentent pas encore leur contenu.

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
