---
title: "Mako Şablonları için Linter ve Biçimlendirici"
description: "djLint, Mako şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için mako profilini ayarlayın."
sidebar:
  label: "Mako"
---

djLint, Mako şablonlarını denetler ve biçimlendirir. Kuralların ve biçimlendirmenin bu şablonlara uyması için `mako` profilini ayarlayın.

**[Mako nedir?](https://www.makotemplates.org/)**

mako profilinde `% if x:` gibi bir kontrol satırı ve `##` yorumu her zaman kendi satırında kalır, öznitelikleri kontrol satırlarına bağlı olan bir etiket de onları yazıldığı gibi korur. Python blokları ile `<%doc>` ve `<%text>` içeriği değiştirilmez; `--format-js` veya `--format-css` ile Mako sözdizimi içeren bir script ya da style da olduğu gibi bırakılır. `% if` ile `% endif` arasındaki satırlar ve her biri kendi satırında duran bir `<%block>` ya da `<%def>` etiketi ile kapanış etiketi arasındaki satırlar, diğer bloklar gibi girintilenir. Bir `${}` ifadesindeki kod yazıldığı gibi kalır.

## Komut satırını kullanma

```bash
djlint /path/to/templates --profile=mako
```

## Ya da bir yapılandırma dosyası kullanın

djLint'i projenizin `pyproject.toml`, `djlint.toml` / `.djlint.toml` ya da `.djlintrc` dosyasında yapılandırın.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::
