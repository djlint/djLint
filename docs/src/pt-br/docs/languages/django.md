---
title: Linter e formatador de templates Django
keywords: django, djlint, linter de templates django, formatador de templates django, formatar templates django
description: O djLint faz o lint e formata templates Django. Defina o perfil django para que as regras e a formatação se ajustem a eles.
tool: django
---

# {{ title }}

{{ description }}

**[O que é Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Usando a linha de comando

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Confira o guia de configuração para ver todas as opções!</a></div>
</div>
