---
title: Linter e formatador de templates Jinja
keywords: jinja, djlint, linter de templates jinja, formatador de templates jinja, formatar templates jinja, minijinja, jinjava, linter de templates minijinja, linter de templates jinjava
description: O djLint faz o lint e formata templates Jinja. Defina o perfil jinja para que as regras e a formatação se ajustem a eles.
tool: jinja
---

# {{ title }}

{{ description }}

**[O que é Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Os templates MiniJinja são totalmente compatíveis com o Jinja2, então use este mesmo perfil `jinja`.

Os templates Jinjava da HubSpot também seguem o estilo do jinja, então use este perfil para eles também.

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
