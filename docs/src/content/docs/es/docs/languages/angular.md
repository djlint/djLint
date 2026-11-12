---
title: "Linter de plantillas de Angular"
description: "djLint analiza plantillas de Angular. Usa el perfil angular para que las reglas se ajusten a ellas."
sidebar:
  label: "Angular"
---

djLint analiza plantillas de Angular. Usa el perfil `angular` para que las reglas se ajusten a ellas.

**[¿Qué es Angular?](https://angular.io/guide/template-syntax)**

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=angular
```

## O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
