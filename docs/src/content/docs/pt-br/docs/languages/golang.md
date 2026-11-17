---
title: "Linter e formatador de templates Go"
description: "O djLint faz o lint e formata templates Go. Defina o perfil golang para que as regras e a formatação se ajustem a eles."
sidebar:
  label: "Templates Go"
---

O djLint faz o lint e formata templates Go. Defina o perfil `golang` para que as regras e a formatação se ajustem a eles.

**[O que são templates Go?](https://pkg.go.dev/text/template)**

Os templates Go (`text/template`, `html/template`) também são a base dos temas do Hugo e dos charts do Helm, então use este mesmo perfil para eles.

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=golang
```

## Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "golang"
```

```toml title="djlint.toml / .djlint.toml"
profile = "golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
