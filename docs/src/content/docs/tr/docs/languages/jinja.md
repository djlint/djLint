---
title: "Jinja Şablonları için Linter ve Biçimlendirici"
description: "djLint hem bir jinja şablon linter'ı hem de bir jinja şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın."
sidebar:
  label: "Jinja"
---

djLint hem bir jinja şablon linter'ı hem de bir jinja şablon biçimlendiricisidir! Şablonlarınızı djLint ile denetlerken ve biçimlendirirken hazır profilden yararlanın.

**[Jinja nedir?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja şablonları Jinja2 ile tamamen uyumludur; bu yüzden aynı `jinja` profilini kullanın.

HubSpot'un Jinjava şablonları da jinja tarzındadır; bu yüzden onlar için de bu profili kullanın.

#### Komut satırını kullanma

```bash
djlint /path/to/templates --profile=jinja
```

#### Ya da bir yapılandırma dosyası kullanın

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

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
