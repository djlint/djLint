---
title: "Linter e formatador de templates Handlebars"
description: "O djLint faz o lint e formata templates Handlebars. Defina o perfil handlebars para que as regras e a formatação se ajustem a eles."
sidebar:
  label: "Handlebars"
---

O djLint faz o lint e formata templates Handlebars. Defina o perfil `handlebars` para que as regras e a formatação se ajustem a eles.

**[O que é Handlebars?](https://handlebarsjs.com/)**

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=handlebars
```

## Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
