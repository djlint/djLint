---
title: "Linter e formatador de templates Jinja"
description: "O djLint faz o lint e formata templates Jinja. Defina o perfil jinja para que as regras e a formatação se ajustem a eles."
sidebar:
  label: "Jinja"
---

O djLint faz o lint e formata templates Jinja. Defina o perfil `jinja` para que as regras e a formatação se ajustem a eles.

**[O que é Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Os templates MiniJinja são totalmente compatíveis com o Jinja2, então use este mesmo perfil `jinja`.

Os templates Jinjava da HubSpot também seguem o estilo do jinja, então use este perfil para eles também.

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=jinja
```

## Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
