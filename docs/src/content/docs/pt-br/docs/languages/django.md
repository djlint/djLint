---
title: "Linter e formatador de templates Django"
description: "O djLint faz o lint e formata templates Django. Defina o perfil django para que as regras e a formatação se ajustem a eles."
sidebar:
  label: "Django"
---

O djLint faz o lint e formata templates Django. Defina o perfil `django` para que as regras e a formatação se ajustem a eles.

**[O que é Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Usando a linha de comando

```bash
djlint /path/to/templates --profile=django
```

## Ou use um arquivo de configuração

Configure o djLint no arquivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` do seu projeto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "django"
```

```toml title="djlint.toml / .djlint.toml"
profile = "django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::
