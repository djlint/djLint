---
title: "Linter e formatador de templates Tera"
description: "O djLint faz o lint e formata templates Tera. Defina o perfil tera para que as regras e a formatação se ajustem a eles."
sidebar:
  label: "Tera"
---

O djLint faz o lint e formata templates Tera. Defina o perfil `tera` para que as regras e a formatação se ajustem a eles.

**[O que é Tera?](https://keats.github.io/tera/)**

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=tera
```

## Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
