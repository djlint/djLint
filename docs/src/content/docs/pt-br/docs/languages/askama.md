---
title: "Linter e formatador de templates Askama"
description: "O djLint é um linter e formatador de templates Askama! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint."
sidebar:
  label: "Askama"
---

O djLint é um linter e formatador de templates Askama! Aproveite o perfil pronto ao fazer o lint e a formatação dos seus templates com o djLint.

**[O que é Askama?](https://askama.readthedocs.io/)**

#### Usando a linha de comando

```bash
djlint /path/to/templates --profile=askama
```

#### Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile="askama"
```

```toml title="djlint.toml / .djlint.toml"
profile="askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
