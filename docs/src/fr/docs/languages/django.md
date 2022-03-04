---
title: Django Template Linter и Formatter
keywords: django, djlint, django template linter, django template formatter, format django templates
description: djLint est un linter de modèles django et un formateur de modèles django ! Profitez du profil pré-construit lorsque vous limez et formatez vos modèles avec djLint.
tool: django
---

# {{ title }}

{{ description }}

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
    <span class="icon is-large"><i class="fas fa-2x fa-arrow-circle-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/fr/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>