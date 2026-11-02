---
title: "Linter y formateador de plantillas de Askama"
description: "¡djLint es un linter y un formateador de plantillas de Askama! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint."
sidebar:
  label: "Askama"
---

¡djLint es un linter y un formateador de plantillas de Askama! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint.

**[¿Qué es Askama?](https://askama.readthedocs.io/)**

#### Desde la línea de comandos

```bash
djlint /path/to/templates --profile=askama
```

#### O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile="askama"
```

```toml title="djlint.toml / .djlint.toml"
profile="askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
