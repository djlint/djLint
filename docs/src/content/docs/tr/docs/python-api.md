---
title: "Python API"
description: "djLint API'si ile şablonları kendi Python kodunuzdan biçimlendirin ve denetleyin."
---

`djlint.api`, bir Python programının içinden metni komut satırıyla aynı sonuçları vererek biçimlendirir ve denetler. Editörler, derleme araçları ve bellekte bir şablon tutan diğer her şey için tasarlanmıştır. Paketteki diğer her şey herhangi bir sürümde değişebilir; bu yüzden `djlint.settings` ya da `djlint.lint` yerine bu modülü kullanın.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, **options)`, bir klasördeki dosyalara uygulanan yapılandırmayı okur. Komut satırının geçerli dizinden yaptığı gibi yapılandırmayı klasörden yukarı doğru arar ve geçerli dizini değiştirmez.

Seçenekler, komut satırı seçeneklerinin adlarını alt çizgili olarak alır ve orada olduğu gibi çalışır: ayarlanmış bir değer yapılandırma dosyasının önüne geçer; `False`, boş bir dize ve çoğu seçenek için `0` ise verilmemiş sayılır. Yollar `pathlib.Path` olarak verilir.

Yapılandırmayı okumak biraz zaman alır; bu yüzden sonucu, okunduğu dosyalar değişmediği sürece saklayın. Sonuç istenen sayıda metin için kullanılabilir.

`python_rules=False` ile `python_module` içeren özel kurallar yüklenmez; bu, güvenmediğiniz bir projenin kodunun çalışmasını önler. Bu kuralların adları `config.skipped_rules` içindedir.

## format_text

`format_text(config, text)` biçimlendirilmiş metni döndürür. İlk satırı CRLF ile biten bir metin CRLF ile, diğer her metin LF ile geri döner. `require_pragma` ile pragma içermeyen bir metin değiştirilmeden geri döner.

## lint_text

`lint_text(config, text, filename="-")`, belgedeki sırasıyla bir `Finding` listesi döndürür. `per-file-ignores`, `filename` ile eşleştirilir. `require_pragma` ile pragma içermeyen bir metnin hiç bulgusu olmaz.

`Finding`, şu alanlara sahip bir adlandırılmış demettir (named tuple):

- `code`: Kuralın kodu, örneğin `H013`.
- `message`: Kuralın söylediği.
- `match`: Kuralın bulduğu metnin başlangıcı, en fazla 20 karakter.
- `line`, `column`: Bulgunun başladığı yer. Satırlar 1'den, sütunlar 0'dan sayılır.
- `end_line`, `end_column`: Bittiği yerin hemen sonrası; bu, daha sonraki bir satırda olabilir.

Sütunlar bayt ya da UTF-16 kod birimi değil, karakter sayar.

## is_excluded

`is_excluded(config, path)`, bir dosyanın komut satırında olduğu gibi `exclude`, `extend_exclude` ya da gitignore tarafından dışarıda bırakılıp bırakılmadığını söyler. `format_text` ve `lint_text` bunu kendileri denetlemez.

## Kural modülleri

Özel bir kuralın `python_module` modülü, yapılandırmanın proje kökünden, süreç başına bir kez içe aktarılır. Çalışmaya devam eden ve birden çok projeyle çalışan bir program, başka bir projenin modüllerini okuyabilmek için projeden içe aktarılan her şeyi `sys.modules` içinden, `sys.path` sonunda kalan proje kökünü de bu listeden kaldırmalıdır.
