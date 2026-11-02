---
title: Linter e formatador de templates Nunjucks
keywords: nunjucks, djlint, linter de templates nunjucks, formatador de templates nunjucks, formatar templates nunjucks, pebble, linter de templates pebble
description: O djLint faz o lint e formata templates Nunjucks. Defina o perfil nunjucks para que as regras e a formatação se ajustem a eles.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[O que é Nunjucks?](https://mozilla.github.io/nunjucks/)**

Os templates Pebble (Java) são compatíveis com o Twig, então use este mesmo perfil para eles.

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
