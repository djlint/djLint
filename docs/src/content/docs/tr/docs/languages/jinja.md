---
title: "Jinja Şablonları için Linter ve Biçimlendirici"
description: "djLint, Jinja şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için jinja profilini ayarlayın."
sidebar:
  label: "Jinja"
---

djLint, Jinja şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `jinja` profilini ayarlayın.

**[Jinja nedir?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja, Jinja2 söz dizimini izler, HubSpot'un Jinjava şablonları da Jinja tarzındadır; bu yüzden ikisi için de `jinja` profilini kullanın. J004 ve J018 Flask'ın `url_for` işlevini önerdiği için Flask kullanmayan bir projede bunları yok sayın.

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=jinja
```

## Yapılandırma dosyasında

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

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
