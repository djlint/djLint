---
title: Linter e formatador de templates Twig
keywords: twig, djlint, linter de templates twig, formatador de templates twig, formatar templates twig, pebble, linter de templates pebble
description: O djLint é um linter e formatador de templates twig! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[O que é Twig?](https://twig.symfony.com/)**

Os templates Pebble (Java) são compatíveis com o Twig, então use este mesmo perfil para eles.

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
