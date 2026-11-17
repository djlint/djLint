---
title: "Linter de templates Angular"
description: "O djLint faz o lint de templates Angular. Defina o perfil angular para que as regras se ajustem a eles."
sidebar:
  label: "Angular"
---

O djLint faz o lint de templates Angular. Defina o perfil `angular` para que as regras se ajustem a eles.

**[O que é Angular?](https://angular.dev/guide/templates)**

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=angular
```

## Em um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```
