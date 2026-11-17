---
title: "Linter y formateador de plantillas de Jinja"
description: "djLint analiza y formatea plantillas de Jinja. Usa el perfil jinja para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Jinja"
---

djLint analiza y formatea plantillas de Jinja. Usa el perfil `jinja` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja sigue la sintaxis de Jinja2, y las plantillas Jinjava de HubSpot también son de estilo Jinja, así que usa el perfil `jinja` para ambas.

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=jinja
```

## En un archivo de configuración

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
