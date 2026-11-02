---
title: Linter et formateur de templates Jinja
keywords: jinja, djlint, linter de templates jinja, formateur de templates jinja, formater des templates jinja, minijinja, jinjava, linter de templates minijinja, linter de templates jinjava
description: djLint linte et formate les templates Jinja. Utilisez le profil jinja pour adapter les règles et le formatage à ces templates.
tool: jinja
---

# {{ title }}

{{ description }}

**[Qu'est-ce que Jinja ?](https://jinja.palletsprojects.com/en/stable/templates/)**

Les templates MiniJinja sont entièrement compatibles avec Jinja2 : utilisez ce même profil `jinja`.

Les templates Jinjava de HubSpot suivent eux aussi le style jinja : utilisez également ce profil pour eux.

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
