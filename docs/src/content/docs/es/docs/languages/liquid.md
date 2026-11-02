---
title: "Linter y formateador de plantillas de Liquid"
description: "djLint analiza y formatea plantillas de Liquid. Usa el perfil liquid para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Liquid"
---

djLint analiza y formatea plantillas de Liquid. Usa el perfil `liquid` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Liquid?](https://shopify.github.io/liquid/)**

Un solo perfil cubre todos los dialectos de Liquid: temas de Shopify, Jekyll, LiquidJS (Eleventy) y Fluid (Orchard Core).

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=liquid
```

## O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
