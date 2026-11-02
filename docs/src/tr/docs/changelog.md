---
description: djLint değişiklik günlüğü. Son sürümlerdeki güncellemeleri ve bir sonraki yükseltmenizde hangi özellikleri bekleyebileceğinizi öğrenin.
title: Değişiklik Günlüğü
keywords: şablon linter'ı, şablon biçimlendiricisi, djLint, HTML, şablonlar, biçimlendirici, linter, değişiklik günlüğü
---

{% raw %}

# Değişiklik Günlüğü

Değişiklik günlüğü artık [sürümlere](https://github.com/djlint/djLint/releases) dahil ediliyor.

## 1.0.2

::: content

- Hata düzeltmeleri [#240](https://github.com/djlint/djLint/issues/240)
:::

## 1.0.1

::: content

- Hata düzeltmeleri [#236](https://github.com/djlint/djLint/issues/236)
:::

## 1.0.0

::: content

- Hata düzeltmeleri [#224](https://github.com/djlint/djLint/issues/224)
:::

## 0.7.6

::: content

- Hata düzeltmeleri [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/197)
- Hataları uyarı olarak döndürmek için `--warn` bayrağı eklendi.
:::

## 0.7.5

::: content

- Hata düzeltmeleri [#187](https://github.com/djlint/djLint/issues/187)
- Şablon dosyalarındaki `yaml` ön bilgisi (front matter) için daha iyi destek eklendi
- [#123](https://github.com/djlint/djLint/issues/123) için T032 kuralı eklendi
- [#124](https://github.com/djlint/djLint/issues/124) için H033 kuralı eklendi
- [#178](https://github.com/djlint/djLint/issues/178) için linter profilleri dışlayıcı yerine kapsayıcı olacak şekilde değiştirildi
- [#188](https://github.com/djlint/djLint/issues/188) için alternatif yapılandırma dosyası seçeneği `.djlintrc` eklendi
:::

## 0.7.4

::: content

- Hata düzeltmeleri [#177](https://github.com/djlint/djLint/issues/177)
:::

## 0.7.3

::: content

- Hata düzeltmeleri [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- `pyproject.toml` dosyasından Py3.6 kaldırıldı.
:::

## 0.7.2

::: content

- Hata düzeltmeleri [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
:::

## 0.7.1

::: content

- Hata düzeltmeleri [#166](https://github.com/djlint/djLint/issues/166)
:::

## 0.7.0

::: content

- Özel HTML etiketleri için yapılandırma eklendi
- Hata düzeltmeleri
:::

## 0.6.9

::: content

- HTML ve Angular profilleri eklendi
- #H023 kuralında bazı varlıklara izin verildi
- Hata düzeltmeleri
:::

## 0.6.8

::: content

- Hata düzeltmeleri
- Belgeler güncellendi
:::

## 0.6.7

::: content

- Özniteliklerin içindeki şablon etiketlerinin biçimlendirilmesi için isteğe bağlı `format_attribute_template_tags` yapılandırma seçeneği eklendi
- Linter mesajı değişkenlerinin sırasını özelleştirmek için `linter_output_format` yapılandırma seçeneği eklendi
- Meta etiketlerini denetlemek için H030 ve H031 kuralları eklendi
:::

## 0.6.6

::: content

- Hata düzeltmeleri
:::

## 0.6.5

::: content

- Çıktı yolları proje köküne göreli olacak şekilde güncellendi
- Hata düzeltmeleri
:::

## 0.6.4

::: content

- Hata düzeltmeleri
:::

## 0.6.3

::: content

- django `blocktrans` etiketi için destek eklendi
- Hata düzeltmeleri
:::

## 0.6.2

::: content

- Hata düzeltmeleri
:::

## 0.6.1

::: content

- Hata düzeltmeleri
- T028 kuralı daha açık bir mesajla daha katı hâle getirildi
:::

## 0.6.0

::: content

- Şablon sözdizimindeki kapatılmamış dizeleri denetlemek için T027 kuralı eklendi
- Özniteliklerdeki eksik boşluksuz etiketleri denetlemek için T028 kuralı eklendi
- Küçük harfli form method değerlerini denetlemek için H029 kuralı eklendi
- "trimmed" içermeyen django blocktranslate etiketleri biçimlendiricide yok sayıldı
- Hata düzeltmeleri
:::

## 0.5.9a

::: content

- python 3.10 için test desteği eklendi
- pre-commit kancası eklendi
:::

## 0.5.9

::: content

- Hariç tutulanları genişletmek için `--use-gitignore` seçeneği eklendi
- Varsayılan hariç tutma eşleştirmesi değiştirildi
- Windows'taki hariç tutma yolları düzeltildi
- Özniteliklerdeki `{%...%}` etiketlerinin biçimlendirilmesi düzeltildi
- Özniteliklerdeki for döngülerinin ve iç içe koşulların biçimlendirilmesi düzeltildi
:::

## 0.5.8

::: content

- require_pragma seçeneği eklendi
- DJ018, input'lardaki `data-src` ve `action` değerlerini de yakalayacak şekilde güncellendi
- Satır içi yok sayma sözdizimi düzeltildi
- Varsayılan kullanım için yer tutucu olarak `--lint` seçeneği eklendi
- Hata düzeltmeleri
:::

## 0.5.7

::: content

- Hata düzeltmeleri
:::

## 0.5.6

::: content

- Boş id ve class etiketlerini bulmak için H026 kuralı eklendi
- Hata düzeltmeleri
:::

## 0.5.5

::: content

- Ayarlar birleştirildi ve kod sadeleştirildi
- Hata düzeltmeleri
:::

## 0.5.4

::: content

- Boş etiket çiftlerini bulmak için H020 kuralı eklendi
- Satır içi stilleri bulmak için H021 kuralı eklendi
- http bağlantılarını bulmak için H022 kuralı eklendi
- Varlık başvurularını bulmak için H023 kuralı eklendi
- Betik ve stillerdeki type özniteliğini bulmak için H024 kuralı eklendi
- Eşi olmayan etiketleri denetlemek için H025 kuralı eklendi. https://stackoverflow.com/a/1736801/10265880 adresine teşekkürler
- Öznitelik biçimlendirmesi iyileştirildi
- `blank_line_after_tag` seçeneği, konumdan bağımsız olarak yeni satır ekleyecek şekilde güncellendi
- django `trans` etiketinin biçimlendirilmesi düzeltildi
- Satır içi stiller için biçimlendirme eklendi
- Özniteliklerin içindeki şablon koşulları için biçimlendirme eklendi
- Linter kurallarına olası bir url konumu olarak srcset eklendi
- Biçimlendirme hızlandırıldı
- [jayvdb](https://github.com/jayvdb)'ye özel teşekkürler
:::

## 0.5.3

::: content

- `--reformat/check` seçeneklerinin stdout çıktısı, girdi olarak stdin kullanıldığında yalnızca yeni html'i yazdıracak şekilde değiştirildi
:::

## 0.5.2

::: content

- `alt` gereksinimi H006'dan ayrılarak H013'e taşındı
- İsteğe bağlı özel kural dosyası eklendi
- Profil seçeneği olarak `golang` eklendi
- Satır içi yorumlar içeren yok sayılmış blokların biçimlendirilmesi düzeltildi
- `--indent` ve `-e` seçeneklerine varsayılan metin eklendi
- URL kuralları # karakterini kabul edecek şekilde güncellendi
- Windows işletim sisteminde dosya kodlaması düzeltildi
- Tek satırlık şablon etiketi regex'i düzeltildi
- Başında boşluk bulunan etiketler için `blank_line_after_tag` düzeltildi
:::

## 0.5.1

::: content

- H019 kuralı eklendi
- DJ018 ve H012'deki hatalar düzeltildi
:::

## 0.5.0

::: content

- Linter kurallarındaki birkaç regex eşleştirme hatası düzeltildi
- Linter'ın yok sayılan bloklarda hata döndürmesi engellendi
- `{% djlint:off %}...{% djlint:on %}` etiketleriyle bir kod bloğunu linter'da/biçimlendiricide yok sayma seçeneği eklendi
:::

## 0.4.9

::: content

- [#35](https://github.com/djlint/djLint/issues/35) numaralı hata düzeltildi
:::

## 0.4.8

::: content

- [#34](https://github.com/djlint/djLint/issues/34) numaralı hata düzeltildi
:::

## 0.4.7

::: content

- `source` etiketi tek satırlık etiketlere taşındı
:::

## 0.4.6

::: content

- [#31](https://github.com/djlint/djLint/issues/31) numaralı hata düzeltildi
:::

## 0.4.5

::: content

- Belgelere en iyi uygulamalar eklendi
- Varsayılan linter/biçimlendirici kurallarını ayarlamak için `--profile` seçeneği eklendi
- jinja url kalıpları için linter kuralları eklendi
:::

## 0.4.4

::: content

- Girinti yapılandırması dizeden tam sayıya değiştirildi. `--indent 3`
:::

## 0.4.3

::: content

- Girinti boşluğu için komut satırı seçeneği eklendi. `--indent=" "`
:::

## 0.4.2

::: content

- `blank_line_after_tag` seçeneğiyle etiketlerden sonra ek boşluk desteği eklendi
:::

## 0.4.1

::: content

- Birden çok dosyayı ya da klasörü tek seferde işleme desteği eklendi
:::

## 0.4.0

::: content

- django `{# ... #}` etiketlerinin biçimlendirilmesi düzeltildi
- figcaption, details ve summary etiketleri için girinti desteği eklendi
- `pyproject.toml` içinde hariç tutulan yollar listesini geçersiz kılma ya da genişletme desteği eklendi
:::

## 0.3.9

::: content

- Öznitelik işleme güncellendi
:::

## 0.3.8

::: content

- stdin desteği eklendi
:::

## 0.3.7

::: content

- `small`, `dt` ve `dd` etiketlerindeki biçimlendirme düzeltildi
:::

## 0.3.6

::: content

- Nunjucks `{%-` açılış blokları için biçimlendirici desteği eklendi
:::

## 0.3.5

::: content

- Daha fazla Django bloğu için destek eklendi
- Özel bloklar için destek eklendi
- `pyproject.toml` içinde yapılandırma desteği eklendi
:::

## 0.3.4

::: content

- Nunjucks boşluksuz etiketi `-%}` biçimi düzeltildi
:::

## 0.3.3

::: content

- Kısa `div` etiketlerinin tek satırda kalmasına izin verildi
:::

## 0.3.2

::: content

- Django yorumlarının biçimlendirilmesi düzeltildi
- textarea biçimlendirmenin dışında bırakıldı
:::

## 0.3.1

::: content

- Öznitelik biçimlendirme regex'i güncellendi
- W010 lint kuralı güncellendi
:::

## 0.3.0

::: content

- Herhangi bir biçimlendirme değişikliği olduysa çıkış kodu 1 olarak değiştirildi
- Jinja `asset` etiketleri için destek eklendi
:::

## 0.2.9

::: content

- W018 regex'i güncellendi
- Yinelenen lint mesajları kaldırıldı
- E001, Handlebars için güncellendi
:::

## 0.2.8

::: content

- Eski Click sürümünde ortaya çıkan ilerleme çubuğu hatası düzeltildi
:::

{% endraw %}
