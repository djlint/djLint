---
title: "Linter e formatador de templates Tera"
description: "O djLint é um linter e formatador de templates Tera! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint."
sidebar:
  label: "Tera"
---

O djLint é um linter e formatador de templates Tera! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint.

**[O que é Tera?](https://keats.github.io/tera/)**

#### Usando a linha de comando

```bash
djlint /path/to/templates --profile=tera
```

#### Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile="tera"
```

```toml title="djlint.toml / .djlint.toml"
profile="tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
