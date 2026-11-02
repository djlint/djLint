---
title: "Linter y formateador de plantillas de Twig"
description: "djLint analiza y formatea plantillas de Twig. Usa el perfil nunjucks para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Twig"
---

djLint analiza y formatea plantillas de Twig. Usa el perfil `nunjucks` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Twig?](https://twig.symfony.com/)**

Las plantillas de Pebble (Java) son compatibles con Twig, así que usa este mismo perfil para ellas.

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=nunjucks
```

## O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
