---
title: Askama Template Linter and Formatter
keywords: askama, rust, djlint, askama template linter, askama template formatter, format askama templates
description: djLint est un linter de modèle Askama et un formateur de modèle Askama ! Profitez du profil pré-construit lorsque vous limez et formatez vos modèles avec djLint.
tool: askama
---

# {{ title }}

{{ description }}

**[C'est quoi Askama?](https://askama.readthedocs.io/)**

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
