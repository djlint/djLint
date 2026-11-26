---
title: "Linter e formatador de templates Nunjucks"
description: "O djLint faz o lint e formata templates Nunjucks. Defina o perfil nunjucks para que as regras e a formatação se ajustem a eles."
sidebar:
  label: "Nunjucks"
---

O djLint faz o lint e formata templates Nunjucks. Defina o perfil `nunjucks` para que as regras e a formatação se ajustem a eles.

**[O que é Nunjucks?](https://mozilla.github.io/nunjucks/)**

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=nunjucks
```

## Em um arquivo de configuração

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
