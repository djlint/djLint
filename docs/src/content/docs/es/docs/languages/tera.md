---
title: "Linter y formateador de plantillas de Tera"
description: "¡djLint es un linter y un formateador de plantillas de Tera! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint."
sidebar:
  label: "Tera"
---

¡djLint es un linter y un formateador de plantillas de Tera! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint.

**[¿Qué es Tera?](https://keats.github.io/tera/)**

#### Desde la línea de comandos

```bash
djlint /path/to/templates --profile=tera
```

#### O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
