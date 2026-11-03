---
title: "Go Şablonları için Linter ve Biçimlendirici"
description: "djLint, Go şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için golang profilini ayarlayın."
sidebar:
  label: "Go şablonları"
---

djLint, Go şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `golang` profilini ayarlayın.

**[Go şablonları nedir?](https://pkg.go.dev/text/template)**

Go şablonları (`text/template`, `html/template`) Hugo temalarının ve Helm chart'larının da temelini oluşturur; bu yüzden onlar için de aynı profili kullanın.

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=golang
```

## Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

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
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
