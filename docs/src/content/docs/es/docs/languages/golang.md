---
title: "Linter y formateador de plantillas de Go"
description: "djLint analiza y formatea plantillas de Go. Usa el perfil golang para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Plantillas de Go"
---

djLint analiza y formatea plantillas de Go. Usa el perfil `golang` para que las reglas y el formato se ajusten a ellas.

**[¿Qué son las plantillas de Go?](https://pkg.go.dev/text/template)**

Las plantillas de Go (`text/template`, `html/template`) también son la base de los temas de Hugo y los charts de Helm, así que usa este mismo perfil para ellos.

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=golang
```

## O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "golang"
```

```toml title="djlint.toml / .djlint.toml"
profile = "golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
