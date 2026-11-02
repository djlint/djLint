---
title: "Linter y formateador de plantillas de Jinja"
description: "¡djLint es un linter y un formateador de plantillas de jinja! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint."
sidebar:
  label: "Jinja"
---

¡djLint es un linter y un formateador de plantillas de jinja! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint.

**[¿Qué es Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Las plantillas de MiniJinja son totalmente compatibles con Jinja2, así que usa este mismo perfil `jinja`.

Las plantillas Jinjava de HubSpot también son de estilo jinja, así que usa también este perfil para ellas.

#### Desde la línea de comandos

```bash
djlint /path/to/templates --profile=jinja
```

#### O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

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
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
