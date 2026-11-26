---
title: "Linter y formateador de plantillas de Nunjucks"
description: "djLint analiza y formatea plantillas de Nunjucks. Usa el perfil nunjucks para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Nunjucks"
---

djLint analiza y formatea plantillas de Nunjucks. Usa el perfil `nunjucks` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Nunjucks?](https://mozilla.github.io/nunjucks/)**

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=nunjucks
```

## En un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

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
