---
title: "Linter y formateador de plantillas de Django"
description: "¡djLint es un linter y un formateador de plantillas de django! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint."
sidebar:
  label: "Django"
---

¡djLint es un linter y un formateador de plantillas de django! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint.

**[¿Qué es Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Desde la línea de comandos

```bash
djlint /path/to/templates --profile=django
```

#### O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
