---
title: "Linter e formatador de templates Twig"
description: "O djLint faz o lint e formata templates Twig. Defina o perfil nunjucks para que as regras e a formatação se ajustem a eles."
sidebar:
  label: "Twig"
---

O djLint faz o lint e formata templates Twig. Defina o perfil `nunjucks` para que as regras e a formatação se ajustem a eles.

**[O que é Twig?](https://twig.symfony.com/)**

Os templates Pebble (Java) são compatíveis com o Twig, então use este mesmo perfil para eles.

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=nunjucks
```

## Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
