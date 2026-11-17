---
title: "Linter e formatador de templates Mako"
description: "O djLint faz o lint e formata templates Mako. Defina o perfil mako para que as regras e a formatação se ajustem a eles."
sidebar:
  label: "Mako"
---

O djLint faz o lint e formata templates Mako. Defina o perfil `mako` para que as regras e a formatação se ajustem a eles.

**[O que é Mako?](https://www.makotemplates.org/)**

Com o perfil mako, uma linha de controle como `% if x:` e um comentário `##` sempre ficam em uma linha própria, e uma tag cujos atributos dependem de linhas de controle os mantém como foram escritos. Blocos de Python e o conteúdo de `<%doc>` e `<%text>` não são alterados, assim como um script ou style que contém sintaxe do Mako com `--format-js` ou `--format-css`. As linhas entre `% if` e `% endif`, e entre uma tag `<%block>` ou `<%def>` e a sua tag de fechamento quando cada uma fica em uma linha própria, são indentadas como qualquer outro bloco. O código de uma expressão `${}` fica como foi escrito.

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=mako
```

## Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
