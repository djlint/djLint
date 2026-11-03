---
title: Linter e formatador de templates Mako
keywords: mako, python, pyramid, open edx, djlint, linter de templates mako, formatador de templates mako, formatar templates mako
description: O djLint faz o lint e formata templates Mako. Defina o perfil mako para que as regras e a formatação se ajustem a eles.
tool: mako
---

# {{ title }}

{{ description }}

**[O que é Mako?](https://www.makotemplates.org/)**

Com o perfil mako, uma linha de controle como `% if x:` e um comentário `##` sempre ficam em uma linha própria, e uma tag cujos atributos dependem de linhas de controle os mantém como foram escritos. Blocos de Python e o conteúdo de `<%doc>` e `<%text>` não são alterados, assim como um script ou style que contém sintaxe do Mako com `--format-js` ou `--format-css`. As linhas de controle ainda não indentam o seu conteúdo.

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
