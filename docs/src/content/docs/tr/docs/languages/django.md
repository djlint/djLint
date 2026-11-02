---
title: "Django Şablonları için Linter ve Biçimlendirici"
description: "djLint, Django şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için django profilini ayarlayın."
sidebar:
  label: "Django"
---

djLint, Django şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `django` profilini ayarlayın.

**[Django nedir?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=django
```

## Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

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
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
