---
title: "Linter e formatador de templates Mustache"
description: "O djLint é um linter e formatador de templates mustache! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint."
sidebar:
  label: "Mustache"
---

O djLint é um linter e formatador de templates mustache! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint.

**[O que é Mustache?](https://mustache.github.io/mustache.5.html)**

#### Usando a linha de comando

```bash
djlint /path/to/templates --profile=handlebars
```

#### Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
