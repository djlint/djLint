---
title: Jinja Template Linter and Formatter
keywords: jinja, djlint, jinja template linter, jinja template formatter, format jinja templates, minijinja, jinjava, minijinja template linter, jinjava template linter
description: djLint est un linter de modèle jinja et un formateur de modèle jinja ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.
tool: jinja
---

# {{ title }}

{{ description }}

**[C'est quoi Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Les modèles MiniJinja sont entièrement compatibles avec Jinja2, utilisez donc ce même profil `jinja`.

Les modèles Jinjava de HubSpot sont également de style jinja, utilisez donc aussi ce profil pour eux.

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
