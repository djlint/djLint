---
title: "Linter y formateador de plantillas de Mustache"
description: "djLint analiza y formatea plantillas de Mustache. Usa el perfil handlebars para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Mustache"
---

djLint analiza y formatea plantillas de Mustache. Usa el perfil `handlebars` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Mustache?](https://mustache.github.io/mustache.5.html)**

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=handlebars
```

## O bien, con un archivo de configuración

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

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
