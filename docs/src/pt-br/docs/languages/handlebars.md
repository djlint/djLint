---
title: Linter e formatador de templates Handlebars
keywords: handlebars, djlint, linter de templates handlebars, formatador de templates handlebars, formatar templates handlebars
description: O djLint é um linter e formatador de templates handlebars! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint.
tool: handlebars
---

# {{ title }}

{{ description }}

**[O que é Handlebars?](https://handlebarsjs.com/)**

#### Usando a linha de comando

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Confira o guia de configuração para ver todas as opções!</a></div>
</div>
