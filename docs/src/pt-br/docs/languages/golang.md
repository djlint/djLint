---
title: Linter e formatador de templates Go
keywords: templates go, golang, djlint, linter de templates go, formatador de templates go, linter de templates golang, formatador de templates golang, formatar templates go, linter de templates hugo, linter de templates helm
description: O djLint faz o lint e formata templates Go. Defina o perfil golang para que as regras e a formatação se ajustem a eles.
tool: golang
---

# {{ title }}

{{ description }}

**[O que são templates Go?](https://pkg.go.dev/text/template)**

Os templates Go (`text/template`, `html/template`) também são a base dos temas do Hugo e dos charts do Helm, então use este mesmo perfil para eles.

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
