---
title: "Linter y formateador de plantillas de Django"
description: "djLint analiza y formatea plantillas de Django. Usa el perfil django para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Django"
---

djLint analiza y formatea plantillas de Django. Usa el perfil `django` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=django
```

## O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

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
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
