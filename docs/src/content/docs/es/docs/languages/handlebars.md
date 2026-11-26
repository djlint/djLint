---
title: "Linter y formateador de plantillas de Handlebars"
description: "djLint analiza y formatea plantillas de Handlebars. Usa el perfil handlebars para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Handlebars"
---

djLint analiza y formatea plantillas de Handlebars. Usa el perfil `handlebars` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Handlebars?](https://handlebarsjs.com/)**

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=handlebars
```

## En un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```
