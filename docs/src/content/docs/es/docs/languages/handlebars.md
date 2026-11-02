---
title: "Linter y formateador de plantillas de Handlebars"
description: "¡djLint es un linter y un formateador de plantillas de handlebars! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint."
sidebar:
  label: "Handlebars"
---

¡djLint es un linter y un formateador de plantillas de handlebars! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint.

**[¿Qué es Handlebars?](https://handlebarsjs.com/)**

#### Desde la línea de comandos

```bash
djlint /path/to/templates --profile=handlebars
```

#### O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
