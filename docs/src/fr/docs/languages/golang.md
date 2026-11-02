---
title: Linter et formateur de templates Go
keywords: templates go, golang, djlint, linter de templates go, formateur de templates go, linter de templates golang, formateur de templates golang, formater des templates go, linter de templates hugo, linter de templates helm
description: djLint est un linter de templates Go et un formateur de templates Go ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.
tool: golang
---

# {{ title }}

{{ description }}

**[Que sont les templates Go ?](https://pkg.go.dev/text/template)**

Les templates Go (`text/template`, `html/template`) servent aussi aux thèmes Hugo et aux charts Helm : utilisez ce même profil pour eux.

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
