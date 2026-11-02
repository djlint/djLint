---
title: Linter e formatador de templates Liquid
keywords: liquid, shopify, jekyll, eleventy, djlint, linter de templates liquid, formatador de templates liquid, formatar templates liquid, shopify, jekyll, eleventy, liquidjs, fluid, linter de temas shopify, linter jekyll
description: O djLint faz o lint e formata templates Liquid. Defina o perfil liquid para que as regras e a formatação se ajustem a eles.
tool: liquid
---

# {{ title }}

{{ description }}

**[O que é Liquid?](https://shopify.github.io/liquid/)**

Um único perfil cobre todos os dialetos do Liquid: temas da Shopify, Jekyll, LiquidJS (Eleventy) e Fluid (Orchard Core).

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
