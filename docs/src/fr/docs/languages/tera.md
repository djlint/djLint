---
title: Tera Template Linter and Formatter
keywords: tera, rust, zola, djlint, tera template linter, tera template formatter, format tera templates
description: djLint est un linter de modèle Tera et un formateur de modèle Tera ! Profitez du profil pré-construit lorsque vous limez et formatez vos modèles avec djLint.
tool: tera
---

# {{ title }}

{{ description }}

**[C'est quoi Tera?](https://keats.github.io/tera/)**

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans votre projet `pyproject.toml`.

```toml
[tool.djlint]
profile="{{ tool }}"
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>
