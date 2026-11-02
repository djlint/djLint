---
title: "Linter e formatador de templates Liquid"
description: "O djLint é um linter e formatador de templates Liquid! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint."
sidebar:
  label: "Liquid"
---

O djLint é um linter e formatador de templates Liquid! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint.

**[O que é Liquid?](https://shopify.github.io/liquid/)**

Um único perfil cobre todos os dialetos do Liquid: temas da Shopify, Jekyll, LiquidJS (Eleventy) e Fluid (Orchard Core).

#### Usando a linha de comando

```bash
djlint /path/to/templates --profile=liquid
```

#### Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile="liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile="liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
