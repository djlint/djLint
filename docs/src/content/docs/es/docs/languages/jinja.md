---
title: "Linter y formateador de plantillas de Jinja"
description: "djLint analiza y formatea plantillas de Jinja. Usa el perfil jinja para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Jinja"
---

djLint analiza y formatea plantillas de Jinja. Usa el perfil `jinja` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Las plantillas de MiniJinja son totalmente compatibles con Jinja2, así que usa este mismo perfil `jinja`.

Las plantillas Jinjava de HubSpot también son de estilo jinja, así que usa también este perfil para ellas.

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=jinja
```

## O bien, con un archivo de configuración

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
