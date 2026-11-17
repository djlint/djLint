---
title: "Linter y formateador de plantillas de Askama"
description: "djLint analiza y formatea plantillas de Askama. Usa el perfil askama para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Askama"
---

djLint analiza y formatea plantillas de Askama. Usa el perfil `askama` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Askama?](https://askama.readthedocs.io/)**

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=askama
```

## O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
