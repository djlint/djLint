---
title: "Linter Kuralları"
description: "djLint HTML şablon linter'ı 30'dan fazla kural içerir! Tanımlarını burada bulabilirsiniz. Özel kurallar ekleyerek kolayca genişletin!"
sidebar:
  label: "Linter"
---

djLint, şablonlarınızın stilini ve geçerliliğini denetleyen birçok kural içerir. Linter'ı, seçtiğiniz şablon dili için hazır bir profili kullanacak şekilde yapılandırarak ondan tam olarak yararlanın.

```bash
djlint /path/to/templates --lint

# özel uzantılarla
djlint /path/to/templates -e html.dj --profile=django

# ya da bir dosya için
djlint /path/to/this.html.j2  --profile=jinja
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::

## Kuralları etkinleştirme ya da devre dışı bırakma

Kuralların çoğu varsayılan olarak etkindir. Kurallar komut satırında `--ignore` bayrağıyla devre dışı bırakılabilir. `--include` bayrağıyla da etkinleştirilebilir.

Örneğin:

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

Bu, [Yapılandırma](/tr/docs/configuration) dosyası üzerinden de yapılabilir.

## Kurallar

| Kod  | Anlamı                                                                                                            | Varsayılan |
| ---- | ----------------------------------------------------------------------------------------------------------------- | ---------- |
| T001 | Değişkenler boşlukla çevrelenmelidir. Örn: `{{ this }}`                                                           | ✔️         |
| T002 | Etiketlerde çift tırnak kullanılmalıdır. Örn `{% extends "this.html" %}`                                          | ✔️         |
| T003 | Endblock bir ad içermelidir. Örn: `{% endblock body %}`.                                                          | -          |
| D004 | (Django) Statik URL'ler `{% static path/to/file %}` kalıbına uymalıdır.                                           | ✔️         |
| J004 | (Jinja) Statik URL'ler `{{ url_for('static'..) }}` kalıbına uymalıdır.                                            | ✔️         |
| H005 | Html etiketinde boş olmayan bir `lang` özniteliği bulunmalıdır.                                                   | ✔️         |
| H006 | `img` etiketinde `height` ve `width` öznitelikleri bulunmalıdır.                                                  | -          |
| H007 | html etiketinden önce `<!DOCTYPE ... >` bulunmalıdır.                                                             | ✔️         |
| H008 | Öznitelikler çift tırnak içinde olmalıdır.                                                                        | ✔️         |
| H009 | Etiket adları küçük harfle yazılmalıdır.                                                                          | ✔️         |
| H010 | Öznitelik adları küçük harfle yazılmalıdır.                                                                       | ✔️         |
| H011 | Öznitelik değerleri tırnak içinde olmalıdır.                                                                      | ✔️         |
| H012 | Öznitelikteki `=` işaretinin çevresinde boşluk olmamalıdır.                                                       | ✔️         |
| H013 | `img` etiketinde alt özniteliği bulunmalıdır.                                                                     | ✔️         |
| H014 | Yapılandırmanın izin verdiğinden daha fazla boş satır var.                                                        | ✔️         |
| H015 | `h` etiketlerinden sonra satır sonu ekleyin.                                                                      | ✔️         |
| H016 | html içinde `title` etiketi eksik.                                                                                | ✔️         |
| H017 | Void etiketler kendiliğinden kapanmalıdır (çakıştığı kural: H018).                                                | -          |
| D018 | (Django) İç bağlantılar `{% url ... %}` kalıbını kullanmalıdır.                                                   | ✔️         |
| H018 | Void etiketler doğası gereği kendiliğinden kapanır ve "/>" ile değil, ">" ile bitmelidir (çakıştığı kural: H017). | -          |
| J018 | (Jinja) İç bağlantılar `{{ url_for() ... }}` kalıbını kullanmalıdır.                                              | ✔️         |
| H019 | `javascript:abc()` yerine `on_` olayı ve gerçek bir URL kullanın.                                                 | ✔️         |
| H020 | Boş etiket çifti bulundu. Kaldırmayı düşünün.                                                                     | ✔️         |
| H021 | Satır içi stillerden kaçınılmalıdır.                                                                              | ✔️         |
| H022 | Dış bağlantılar için HTTPS kullanın.                                                                              | ✔️         |
| H023 | Varlık başvuruları (entity reference) kullanmayın.                                                                | ✔️         |
| H024 | Betiklerde ve stillerde type belirtmeyin.                                                                         | ✔️         |
| H025 | Etiketin eşi yok gibi görünüyor.                                                                                  | ✔️         |
| H026 | Boş id ve class öznitelikleri kaldırılabilir.                                                                     | ✔️         |
| T027 | Şablon sözdiziminde kapatılmamış dize bulundu.                                                                    | ✔️         |
| T028 | Öznitelik değerlerinin içinde boşluksuz etiketler kullanmayı düşünün. `{%- if/for -%}`                            | -          |
| H029 | Form method değerlerini küçük harfle yazmayı düşünün.                                                             | ✔️         |
| H030 | Bir meta açıklaması (description) eklemeyi düşünün.                                                               | ✔️         |
| T032 | Şablon etiketlerinde fazladan boşluk bulundu.                                                                     | ✔️         |
| H033 | Form action değerinde fazladan boşluk bulundu.                                                                    | ✔️         |
| T034 | {% ... }% yerine {% ... %} mi kullanmak istediniz?                                                                | ✔️         |
| H036 | Boşluk vermek için `br` etiketleri kullanmayın.                                                                   | ✔️         |
| H037 | Yinelenen öznitelik bulundu.                                                                                      | ✔️         |
| T038 | Blok etiketinin eşleşen bir bitiş etiketi yok.                                                                    | ✔️         |
| T039 | Kapatılmamış şablon etiketi bulundu.                                                                              | ✔️         |
| T040 | extends ya da include etiketinde şablon adı eksik ya da boş.                                                      | ✔️         |
| H041 | Etiket, açıldığı şablon bloğundan farklı bir blokta kapatılmış.                                                   | ✔️         |
| T041 | Extends etiketi şablondaki ilk etiket olmalıdır.                                                                  | ✔️         |
| H042 | Label etiketinin for özniteliğiyle eşleşen bir öğe id'si bu dosyada yok.                                          | ✔️         |
| T042 | Başka bir şablonu genişleten bir şablonda, blok dışındaki içerik işlenmez.                                        | ✔️         |
| H043 | Button etiketinde bir `type` özniteliği bulunmalıdır.                                                             | ✔️         |
| T043 | Blok adı şablonda birden fazla kez kullanılmış.                                                                   | ✔️         |
| H044 | Thead içinde `th` ve `td` hücreleri karıştırılmamalıdır.                                                          | ✔️         |
| T044 | Çıktı etiketi bir deyim anahtar sözcüğü içeriyor; bir blok etiketi kullanın.                                      | ✔️         |
| H045 | Iframe etiketinde bir `title` özniteliği bulunmalıdır.                                                            | ✔️         |
| T045 | Html yorumunun içindeki şablon etiketi yine de çalışır; devre dışı bırakmak için şablon yorumu kullanın.          | ✔️         |
| H046 | Tabindex pozitif olmamalıdır.                                                                                     | ✔️         |
| H047 | Odaklanılabilir bir öğede aria-hidden ayarlanmamalıdır.                                                           | ✔️         |
| H048 | Aria özniteliği, belirtimin tanımladıklarından biri değil.                                                        | ✔️         |
| H049 | Viewport, sayfanın yakınlaştırılmasını engellememelidir.                                                          | ✔️         |
| H050 | Öğe eskimiştir ve başka bir öğeyle değiştirilmelidir.                                                             | ✔️         |
| H051 | Role, ARIA'nın işaretleme için tanımladığı rollerden biri değil.                                                  | ✔️         |
| H052 | Meta refresh, sayfayı bir zamanlayıcıyla yeniden yüklememeli ya da yönlendirmemelidir.                            | ✔️         |
| H053 | Id dosyada birden fazla kez kullanılmış.                                                                          | ✔️         |
| H054 | Etkileşimli öğe, başka bir etkileşimli öğenin içine yerleştirilmemelidir.                                         | ✔️         |
| H055 | Lang özniteliği en ya da pt-BR gibi bir dil etiketi olmalıdır.                                                    | ✔️         |
| H056 | Src boş olmamalıdır.                                                                                              | ✔️         |
| H057 | Videoda bir altyazı (captions) izi bulunmalıdır.                                                                  | ✔️         |

### Kod kalıpları

Bir kodun ilk harfi şu kalıbı izler:

- D: yalnızca Django'ya özgüdür
- H: html'e uygulanır
- J: yalnızca Jinja'ya özgüdür
- M: yalnızca Handlebars'a özgüdür
- N: yalnızca Nunjucks'a özgüdür
- T: genel olarak şablonlara uygulanır

### Kural ayrıntıları

<!-- oxfmt-ignore-start -->

#### T001

`Variables should be wrapped in a whitespace.`

İç boşluk bırakılmadan yazılan `{{user.name}}` gibi şablon sözdizimini taramak ve diff'lerde incelemek daha zordur. Kod tabanı genelinde tutarsız boşluk kullanımı da grep tabanlı yeniden düzenlemeleri (bir değişkeni ya da etiketi aramayı) güvenilmez kılar, çünkü aynı ifade birden fazla yazımla var olur. Django ve Jinja stil kılavuzlarının ikisi de `{{ var }}` ve `{% tag %}` biçiminde tek boşluk kullanır.

handlebars ve golang profillerinde uygulanmaz.

Yapmayın:

```html
{{user.name}}
```

Yapın:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Şablon etiketlerinde (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) tek ve çift tırnağı karışık kullanmak, aynı şablon adının iki farklı yazımla görünmesine yol açar; böylece aramalar ve toplu yeniden adlandırmalar geçtiği yerlerin yarısını kaçırır. Çift tırnakta karar kılmak, etiket argümanlarını dosyanın geri kalanındaki HTML öznitelik tırnaklarıyla tutarlı tutar.

HTML öznitelik değerlerinin içindeki tek tırnaklar (örn. `<span title="{% trans 'x' %}">`) bildirilmez, çünkü özniteliğin çift tırnakları orada tek tırnak kullanmayı zorunlu kılar.

`quote_style = "single"` ile kural bunun yerine tek tırnak ister ve biçimlendirici de tek tırnak yazar.

`--reformat` bu tırnakları sizin yerinize yeniden yazar; bu yüzden bir bulgu hiçbir zaman elle yapılacak bir iş değildir.

Yapmayın:

```html
{% extends 'base.html' %}
```

Yapın:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

Bir `{% block %}` çok sayıda satıra yayıldığında ya da bloklar iç içe olduğunda, yalın bir `{% endblock %}` hangi bloğu kapattığına dair hiçbir ipucu vermez; bu yüzden düzenleme sırasında yanlış bloğu kapatmak kolaydır ve alt şablonlar da yanlış içeriği geçersiz kılar. Endblock'u adlandırmak eşleşmeyi belgeler ve hem djLint'in hem de Django'nun (eşleşmeyen bir endblock adında TemplateSyntaxError fırlatır) yanlış yerde kapatılmış bir bloğu yakalamasını sağlar. Eşleştirme hataları (kapatılmamış bloklar, eşi olmayan endblock'lar ve eşleşmeyen adlar) T038'in ele aldığı doğruluk denetimleridir.

Varsayılan olarak kapalıdır; `--include=T003` ile etkinleştirin. `--name-endblocks` adı sizin yerinize yazar; bu yüzden bir bulgu hiçbir zaman elle yapılacak bir iş değildir.

Blok aynı satırda açılıp kapanıyorsa ad gerekmez, örn. `{% block title %}``{% endblock %}`. Biçimlendirici, başka etiketler içeren bir bloğun içeriğini ayrı satırlara taşır; bu yüzden tek satırda yazılmış bir blok biçimlendirildikten sonra bir ad gerektirebilir. `--name-endblocks` ile biçimlendirici bu adı da yazar.

Yapmayın:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

Yapın:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

/static/ yollarını sabit kodlamak Django'nun `{% static %}` etiketini devre dışı bırakır; böylece STATIC_URL değiştiğinde (örn. varlıklar bir CDN'e ya da bir alt yolda dağıtıma taşındığında) şablonlar bozulur ve ManifestStaticFilesStorage'ın ürettiği hash'li dosya adları hiçbir zaman kullanılmaz; bu da üretimde 404'lere ya da önbellekte kalmış eski varlıklara yol açar. Kural birebir `/static/` önekini arar; bu yüzden statik dosyalarını başka bir yoldan sunan projeler kapsanmaz.

Yapmayın:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Yapın:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

/static/ yollarını sabit kodlamak Flask/Jinja'nın url_for('static', ...) işlevini devre dışı bırakır; böylece uygulama bir URL önekinin altına bağlandığında ya da statik klasör veya sunucu değiştirildiğinde varlıklar 404 verir ve çatının eklediği önbellek kırma (cache-busting) sorgu dizeleri kaybolur. Kural birebir `/static/` önekini arar; bu yüzden statik dosyalarını başka bir yoldan sunan projeler kapsanmaz.

Yapmayın:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Yapın:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

`<html>` üzerinde bir lang özniteliği olmadığında ekran okuyucular telaffuz kurallarını tahmin eder ve sayfayı yanlış dilde okuyabilir; tarayıcılar da çeviriyi, heceleme ile satır sonu bölmeyi ya da yerel ayara uygun tırnak işaretlerini doğru şekilde sunamaz. Sayfa dilini bildirmek WCAG 2.1'in 3.1.1 başarı ölçütüdür (Düzey A).

`lang=""` ve değersiz bir `lang` ikisi de dilin bilinmediğini söyler; bu yüzden eksik bir öznitelikle aynı şekilde bildirilir.

Yapmayın:

```html
<!DOCTYPE html>
<html>
</html>
```

Yapın:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Varsayılan olarak kapalıdır; `--include=H006` ile etkinleştirin.

Bir `<img>` öğesinin genişliği ve yüksekliği olmadığında tarayıcı, görsel inmeden önce ona yer ayıramaz; bu yüzden görseller yüklendikçe çevredeki içerik kayar. Bu düzen kayması Cumulative Layout Shift (bir Core Web Vitals metriği) değerini kötüleştirir ve sayfa yerine oturana kadar kullanıcıların yanlış yere tıklamasına neden olabilir.

Yapmayın:

```html
<img src="cat.png" alt="Cat">
```

Yapın:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

`<html>` etiketinden önce bir `<!DOCTYPE>` olmadığında tarayıcılar sayfayı eski kutu modeli ve yerleşim davranışını taklit eden quirks modunda çizer; bu yüzden CSS tarayıcılar arasında tutarsız görüntülenir. Doctype'tan önce gelen şablon etiketleri ve yorumlar sorun değildir; yalnızca `<html>` etiketinin kendisinden önce doctype gelmelidir.

Yapmayın:

```html
<html lang="en">
</html>
```

Yapın:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Karışık tırnak stilleri öznitelik değerlerini taramayı ve grep ile aramayı zorlaştırır; tek tırnaklı değerler de içerik bir kesme işareti içerdiği anda bozulur. Çift tırnak; HTML belirtimlerinin, biçimlendiricilerin ve çoğu stil kılavuzunun kullandığı kuraldır; bu yüzden çift tırnakta karar kılmak şablonları daha geniş ekosistemle tutarlı tutar.

Yapmayın:

```html
<div class='content'></div>
```

Yapın:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

HTML ayrıştırıcıları büyük harfli etiket adlarını kabul eder, ancak XHTML ve XML serileştirmeleri büyük/küçük harfe duyarlıdır ve bunları reddeder; karışık harf kullanımı da metin aramayı ve diff incelemesini güvenilmez kılar (`<h1>` için grep yapmak `<H1>`'i kaçırır). Küçük harfli etiket adları şablonları taşınabilir ve tutarlı tutar.

Biçimlendiriciye harf büyüklüğüne dokunmamasını söyleyen `--ignore-case` altında bildirilmez.

Yapmayın:

```html
<H1>Welcome</H1>
```

Yapın:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

Büyük harfli öznitelik adları XHTML/XML serileştirmelerinde geçersizdir ve şablonlar genelinde metin aramayı boşa çıkarır (src= için grep yapmak SRC='yi kaçırır). DOM, HTML öznitelik adlarını zaten küçük harfe dönüştürür; bu yüzden büyük harfli yazımlar hiçbir fayda sağlamadan tutarsızlık katar. Yalnızca biçimlendiricinin küçük harfe çevirdiği adlar bildirilir: `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media` ve `srcset`. `--reformat` bunları sizin yerinize düzeltir; `:itemID` gibi bir çatı bağlaması ya da `data-ID` gibi daha uzun bir ad ise harf büyüklüğünü korur.

Biçimlendiriciye harf büyüklüğüne dokunmamasını söyleyen `--ignore-case` altında bildirilmez.

Yapmayın:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

Yapın:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

Tırnaksız öznitelik değerleri ilk boşlukta biter; bu yüzden class=btn primary gibi bir değer, boşluktan sonraki her şeyi sessizce düşürür (tarayıcı "primary" değerini ayrı bir boolean öznitelik olarak ele alır). Şablon değişkenlerinden gelen değerler özellikle kırılgandır: işlenen herhangi bir boşluk, "=" ya da ">" etiketi bozar. Tırnak kullanmak değerin sınırını açık ve güvenli hâle getirir.

Yapmayın:

```html
<div class=test></div>
```

Yapın:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

"=" çevresinde boşluk olduğunda etiket üç ayrı parça gibi okunur ve dağılmaya tek bir düzenleme uzaklıktadır: ortadan yapılan bir satır kaydırma ya da kesme, geride yalın bir boolean öznitelik ve başıboş bir metin bırakır. name="value" yazımını bitişik tutmak, basit metin araçlarının (grep, bul ve değiştir) da varsaydığı şeydir; bu yüzden karışık boşluk kullanımı öznitelikleri güvenilir şekilde bulmayı ve yeniden düzenlemeyi zorlaştırır. `--reformat` bu boşlukları sizin yerinize kaldırır.

Yapmayın:

```html
<div class = "test"></div>
```

Yapın:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Bir alt özniteliği olmadığında ekran okuyucular görselin dosya adını okur ya da hiçbir şey söylemez; bu da WCAG 1.1.1'i (Metin Dışı İçerik) karşılamaz. Alt metni, görsel yüklenemediğinde kullanıcıların gördüğü şeydir de. Dekoratif görseller, yardımcı teknolojilerin onları atlaması gerektiğini bilmesi için açıkça boş bir alt="" taşımalıdır; bu da bu kuralı karşılar.

Değersiz bir `alt`, dekoratif görsel durumu olan `alt=""` ile aynıdır; bu yüzden kabul edilir.

Yapmayın:

```html
<img src="cat.jpg" height="200" width="300">
```

Yapın:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Art arda gelen boş satırların işlenen sayfa üzerinde hiçbir etkisi yoktur (HTML boşlukları daraltır), ancak şablonları şişirir ve komşu satırlar değiştiğinde gürültülü diff'ler oluşturur. djLint'in biçimlendiricisi bunları varsayılan olarak tamamen kaldırır (en fazla `max_blank_lines` kadar boş satır bırakır; bunun varsayılan değeri 0'dır); bu yüzden kalan boş satır dizileri biçimlendirilmemiş koda işaret eder.

Yapmayın:

```html
<div>one</div>


<p>two</p>
```

Yapın:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

Başlıklar, belge ana hatlarını tanımlayan blok düzeyinde yer işaretleridir; bir sonraki öğeyi kapanan h etiketiyle aynı satıra sıkıştırmak bu yapıyı kaynakta gizler ve iki öğeden birinde yapılan düzenlemelerin diff'lerde ikisinde birden değişiklik gibi görünmesine yol açar. Her başlıktan sonra bir satır sonu, şablonun görsel yapısını işlenen ana hatlarla uyumlu tutar.

Yapmayın:

```html
<h1>Heading</h1><p>Intro text.</p>
```

Yapın:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

HTML belirtimi her belgede bir title öğesi bulunmasını şart koşar. Bu öğe olmadığında tarayıcı sekmeleri, yer imleri ve geçmiş sayfa adı yerine çıplak bir URL gösterir, arama motorları sayfanın birincil etiketini kaybeder ve ekran okuyucu kullanıcıları sayfa yüklendiğinde duyurulan ilk şeyi kaybeder; bu da WCAG 2.4.2'yi (Sayfa Başlığı, Düzey A) karşılamaz.

Yalnızca eksiksiz bir `<html>`...`</html>` belgesi içeren dosyalarda tetiklenir; bu yüzden kısmi şablonlar ve bir temel şablonu genişleten alt şablonlar hiçbir zaman bildirilmez. Başlığı istemci tarafında ayarlayan SPA kabukları da yine statik bir `<title>` gerektirir: ilk çizimde, tarayıcı robotlarında ve JavaScript başarısız olduğunda görünen odur.

Yapmayın:

```html
<html lang="en">
<body>Content</body>
</html>
```

Yapın:

```html
<html lang="en">
<head>
<title>My page</title>
</head>
<body>Content</body>
</html>
```

#### H017

`Void tags should be self closing.`

XML/XHTML olarak da ayrıştırılması gereken (ya da XML tabanlı araçlara verilen) şablonlar, kapanış eğik çizgisi olmadan yazılmış void öğeleri reddeder; kod tabanı genelinde `<br>` ile `<br />` yazımını karıştırmak da tutarsız diff'ler üretir. Bu kural, her void öğenin aynı şekilde kapatılması için XHTML tarzı kuralı zorunlu kılar.

Varsayılan olarak kapalıdır; `--include=H017` ile etkinleştirin. H018 ile birbirini dışlar; iki kuraldan yalnızca birini etkinleştirin. `--close-void-tags`, html void etiketlerine eğik çizgiyi sizin yerinize ekler. Bir svg `<path>` yazıldığı gibi bırakılır; bu yüzden onu elle kapatın.

Yapmayın:

```html
<br>
<meta charset="utf-8">
```

Yapın:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

Sabit kodlanmış iç URL'ler, urls.py içinde bir rotanın yolu değiştiğinde sessizce eskir; bu da URLconf üzerindeki hiçbir testin yakalamayacağı bozuk bağlantılara ve ölü form action'larına yol açar. `{% url %}` yolu rota adından çözümler; böylece bir yolu yeniden adlandırmak tüm bağlantıları bir kerede günceller.

Yapmayın:

```html
<a href="/accounts/login">Login</a>
```

Yapın:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

HTML yaşayan standardında bir void öğenin sonundaki eğik çizginin hiçbir anlamı yoktur (ayrıştırıcı onu yok sayar); bu yüzden `<br />` yazmak, HTML'de olmayan XML tarzı kendiliğinden kapanma davranışını ima eder ve okuyucuları void olmayan etiketlere de eğik çizgi eklemeye yöneltebilir; orada başıboş bir / sessizce atılır ve kapatılmamış etiket hatalarını gizler. Bu kural, void öğelerin yalın > ile bitmesini zorunlu kılar.

Varsayılan olarak kapalıdır; `--include=H018` ile etkinleştirin. H017 ile birbirini dışlar; iki kuraldan yalnızca birini etkinleştirin. SVG `<path />` muaftır, çünkü SVG bir XML'dir ve eğik çizgiyi gerektirir. Biçimlendirici bu kuralın bildirdiği eğik çizgiyi yazacağından `--close-void-tags` altında bildirilmez.

Yapmayın:

```html
<br />
<meta charset="utf-8" />
```

Yapın:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

Sabit kodlanmış iç URL'ler, bir rotanın yolu değiştiğinde ya da uygulama bir önekin altına bağlandığında sessizce bozulur; geride ölü bağlantılar ve 404'e gönderim yapan form action'ları kalır. url_for() URL'yi uç nokta adından oluşturur; böylece rota değişiklikleri her şablona otomatik olarak yansır.

Yapmayın:

```html
<a href="/accounts/login">Login</a>
```

Yapın:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

javascript: URL'leri orta tıklamayı ve yeni sekmede açmayı bozar, JavaScript devre dışıyken ya da yüklenemediğinde hiçbir şey yapmaz, katı Content Security Policy'ler tarafından engellenir ve klasik bir XSS enjeksiyon noktasıdır. Bunun yerine href için gerçek bir URL kullanın ve davranışı bir olay işleyicisiyle bağlayın. Katı bir CSP altında satır içi on* işleyicileri de engellenir: gösterilen onclick, şablon içindeki en küçük düzeltmedir; dinleyiciyi bir betik dosyasından addEventListener ile bağlamayı tercih edin.

Yapmayın:

```html
<a href="javascript:openPopup()">Open popup</a>
```

Yapın:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

Boş bir etiket çifti hiçbir içerik göstermez, ancak yine de stil sayfalarından kenar boşluğu, kenarlık ya da flex/grid aralıkları alabilen bir DOM düğümü oluşturur; bu da izini sürmesi zor hayalet boşluklar üretir. Genellikle daha önceki bir düzenlemeden kalmış işaretlemedir. Normal işaretlemede meşru olarak boş olan etiketler (td, th, li, dt, dd, slot) muaftır. Herhangi bir öznitelik taşıyan etiketler de (`<div id="app">``</div>` gibi JS bağlama noktaları, `<i class="fa fa-user">``</i>` gibi simge yazı tipi öğeleri) bildirilmez; yalnızca hiç özniteliği olmayan boş çiftler eşleşir.

Yapmayın:

```html
<p>Saved.</p>
<span> </span>
```

Yapın:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Satır içi stiller herhangi bir stil sayfası seçicisinden daha yüksek özgüllüğe sahiptir; bu yüzden onları daha sonra geçersiz kılmak !important gerektirir. style-src içinde 'unsafe-inline' olmayan Content Security Policy'ler tarafından engellenirler ve sunumu şablonlar arasına dağıtırlar; böylece bir tema ya da tasarım değişikliği tek bir stil sayfası yerine işaretlemeyi düzenlemek anlamına gelir. Bildirimi bir CSS sınıfına taşıyın. Meşru bir istisna: birçok e-posta istemcisinin `<style>` bloklarını kaldırdığı ve satır içi stillerin standart teknik olduğu HTML e-posta şablonları. E-posta şablonu dizinlerinizi hariç tutun ya da bu kuralı onlar için devre dışı bırakın.

Yapmayın:

```html
<div style="color: red;">Wrong username or password.</div>
```

Yapın:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

HTTPS üzerinden sunulan bir sayfadaki düz http:// alt kaynakları karma içeriktir: tarayıcılar betikleri, stil sayfalarını ve iframe'leri doğrudan engeller, görsellerde ise bağlantıyı otomatik olarak yükseltir ya da uyarı verir. Bir http:// sayfasına giden `<a>` bağlantısı karma içerik değildir, ancak ziyaretçileri yine de araya girmeye ve kurcalamaya açık şifrelenmemiş bir bağlantı üzerinden gönderir. Gerçekten TLS'si olmayan iç sunuculara yapılan başvurular da bildirilir; kuralı devre dışı bırakmak yerine bu yerleri bir `{# djlint:off H022 #}` bloğuyla susturun.

Yapmayın:

```html
<a href="http://example.com">Example</a>
```

Yapın:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

HTML5 belgeleri UTF-8'dir; bu yüzden karakterin kendisi her yerde çalışır ve inceleyenlerin gerçekte okuduğu da odur. Bir varlık başvurusundaki yazım hatası (örn. `&mdsah;`) tarayıcı tarafından yakalanmaz ve olduğu gibi bozuk metin olarak görüntülenir. djLint, sözdizimi taşıyan varlıklara (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;` ve açık yazıldığında bir şablon sınırlayıcısını tamamlayacak olan `&percnt;`, `&num;` ve `&dollar;` ile birlikte `&lbrace;` ve `&rbrace;` küme parantezleri) ve görünmez olduğu için karakterin kendisi olarak incelenemeyecek bir karakteri adlandıran varlıklara izin verir: boşluklar (`&nbsp;`, `&thinsp;`, `&hairsp;`), birleştiriciler ve işaretler (`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`) ve `&shy;`; adlandırılmış, ondalık ve onaltılık biçimlerin hepsinde.

`--reformat`, varlığı sizin yerinize karakter olarak yeniden yazar; bu yüzden bir bulgu hiçbir zaman elle yapılacak bir iş değildir. Bir şablon etiketinin içine yazılmış bir varlık, sayfanın değil etiketin parçasıdır; bu yüzden ne kural ne de biçimlendirici ona dokunur. `--no-entity-formatting` yeniden yazmayı kapatır ama kuralı açık bırakır; böylece varlık yine de bildirilir. Varlıkları korumak için `ignore` listesine `H023` ekleyin.

Yapmayın:

```html
<p>Dates 1900 &mdash; 2000</p>
```

Yapın:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript ve text/css, `<script>` ve `<style>` için HTML5 varsayılanlarıdır; bu yüzden bu öznitelik, tarayıcının yok saydığı ölü bir yüktür ve WHATWG belirtimi açıkça yazılmamasını söyler. Özniteliği kaldırmak, modül betiklerine (type="module" değerinin gerçekten önemli olduğu yer) kopyalandığında öğeyi bozan eskimiş MIME dizelerinden de kaçınmayı sağlar.

Yapmayın:

```html
<script type="text/javascript" src="app.js">
```

Yapın:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

Eşleşen açılış ya da kapanış etiketi olmayan bir etiket, tarayıcının hata düzeltme mekanizmasını öğenin nerede bittiğini tahmin etmeye zorlar; böylece ardından gelen işaretleme yanlış öğenin içine yutulur. Yerleşim, CSS seçicileri ve JavaScript DOM sorguları da sessizce ve tarayıcıdan tarayıcıya farklı şekilde bozulur. H025, bir `<p>` içinde açılan `<ol>` ya da `<ul>` öğesini de bildirir: HTML ayrıştırıcısı paragrafı listeden önce kapatır, bu yüzden işaretleme hiçbir zaman yazıldığı gibi iç içe geçmez.

Yapmayın:

```html
<div>
  <p>Hello</p>
```

Yapın:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

Hiçbir class ya da id seçicisi boş bir öznitelikle eşleşmez ve boş bir id geçersiz HTML'dir (id değeri boş dize olmamalıdır). `div[class]` gibi bir öznitelik varlığı seçicisi ise yine de onunla eşleşir; bu yüzden böyle yazılmış bir stil sayfası, özniteliğin kaldırılmasını fark eder. Boş öznitelik genellikle bir değişkenin yerleştirilmesi amaçlanan bir şablon hatasına işaret eder; bu yüzden onu kaldırmak ya da doldurmak, bu hatanın göz önünde saklanmasını önler.

Yapmayın:

```html
<div id="" class="">content</div>
```

Yapın:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

`{% ... %}` ya da `{{ ... }}` içinde açılıp hiç kapatılmayan bir tırnak, şablon motorunun etiketi yanlış ayrıştırmasına neden olur: Django ve Jinja ya işleme sırasında TemplateSyntaxError fırlatır ya da etiketin geri kalan argümanlarını sessizce dize içeriği olarak yutar; böylece sayfa 500 hatası verir ya da eksik argümanlarla işlenir.

Yapmayın:

```html
{% trans "Welcome %}
```

Yapın:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Varsayılan olarak kapalıdır; `--include=T028` ile etkinleştirin.

Boşluksuz bir etiketin kaldırdığı boşluk, çıktıda görünen boşluktur; bu yüzden bunu yalnızca özniteliğin kaybedecek boşluğu olmadığı yerlerde uygulayın. `alt="{%- if brand -%}Acme{%- endif -%} logo"` çıktıda `Acmelogo` olur ve bir svg `d="M12 {%- if big -%}20{%- endif -%} 4Z"` farklı bir yola dönüşür. Kuralın isteğe bağlı olmasının nedeni budur.

Bir öznitelik değerinin içindeki şablon etiketleri, çevrelerindeki boşlukları ve satır sonlarını işlenen özniteliğe yansıtır; bu yüzden düz `{% if %}`/`{% for %}` etiketleriyle oluşturulan bir href ya da src başıboş boşluklar içerebilir ve bozuk URL'ler üretebilir. Jinja/Nunjucks boşluk denetimi etiketleri (`{%- ... -%}`) bu çevreleyen boşlukları kaldırır; böylece öznitelik tek ve temiz bir değer olarak işlenir. class özniteliği muaftır, çünkü sınıf adları arasındaki fazladan boşluk zararsızdır.

django profilinde uygulanmaz: Django şablon etiketleri `{%- -%}` boşluk denetimini desteklemez.

Yapmayın:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

Yapın:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

HTML belirtimi form method anahtar sözcüklerini küçük harfle tanımlar (get, post); tarayıcılar büyük harfli biçimleri yalnızca büyük/küçük harfe duyarsız bir geri dönüş eşleştirmesiyle kabul eder. Standart küçük harfli biçimi korumak şablonları tutarlı ve grep ile aranabilir tutar, katı doğrulayıcıların ve XHTML tabanlı araç zincirlerinin şikâyetlerinden de kaçınır.

Yapmayın:

```html
<form method="POST"></form>
```

Yapın:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

Arama motorları meta açıklamasını sonuçlarda sayfa başlığınızın altındaki kısa metin olarak kullanır; açıklama olmadığında bu metni sayfadaki rastgele bir metinden kendileri oluşturur. Bu da tıklama oranlarını düşürür ve sayfa paylaşıldığında kötü bağlantı önizlemeleri üretir.

Yalnızca eksiksiz bir `<html>`...`</html>` belgesi içeren dosyalarda tetiklenir. Kısa metin gerekçesi herkese açık olarak dizinlenen sayfalar için geçerlidir; kimlik doğrulama arkasındaki ya da intranet uygulamalarında bu kural genellikle devre dışı bırakılır.

Yapmayın:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

Yapın:

```html
<html lang="en">
  <head>
    <title>Home</title>
    <meta name="description" content="A short summary of this page.">
  </head>
  <body>Welcome</body>
</html>
```

#### T032

`Extra whitespace found in template tags.`

Bir şablon etiketinin argümanları arasındaki art arda boşluklar ya da sekmeler görünmez bir gürültüdür: diff'lerdeki gerçek farkları gizler, eksik bir argümanı fark etmeyi zorlaştırabilir ve djLint'in biçimlendiricisinin ürettiği tek boşluklu stilden saparak gereksiz yeniden biçimlendirme değişikliklerine yol açar. Tırnaklı dizelerin içindeki boşluklar korunur ve bildirilmez.

Yapmayın:

```html
{% static  'css/style.css' %}
```

Yapın:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Bir formun action değerinin başındaki ya da sonundaki boşluk, işlenen URL'nin parçası olur. Tarayıcılar ayrıştırırken bu boşluğu kırpar, ancak tarayıcı dışı istemciler ve değeri olduğu gibi kullanan testler kırpmayabilir; bir `{% url %}` etiketinin çevresindeki başıboş boşluk da neredeyse her zaman, sunucu tarafındaki rota eşleştirmesinde başarısız olan bir gönderim URL'si üreten bir yazım hatasına işaret eder.

Yapmayın:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

Yapın:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% neredeyse her zaman %} yerine yapılmış bir yazım hatasıdır. Şablon motoru }% dizisini etiket sınırlayıcısı olarak tanımaz, bu yüzden etiket hiçbir zaman ayrıştırılmaz: ham {% ... }% metni işlenen HTML'e sızar ya da motor kapatılmamış etikete ulaştığında bir sözdizimi hatası fırlatır.

Yapmayın:

```html
{% include "footer.html" }%
```

Yapın:

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

Html belirtimi `<br>` etiketine yalnızca bir posta adresinde ya da bir şiirde olduğu gibi içeriğin kendisinin parçası olan bir satır sonu için izin verir ve bu kullanıma dokunulmaz. Bildirilen, belirtimin yasakladığı sunumsal kullanımdır: dikey boşluk anlamına gelen iki ya da daha fazla art arda satır sonu ve bir blok öğenin iç kenarına dayanan, öğenin kendi kenar boşluğunun zaten vermeyeceği hiçbir şeyi göstermeyen bir satır sonu. İkisi de dar genişliklerde metnin yeniden akışını bozar ve ekran okuyucu, duyurulacak bir şey olmayan yerde zorunlu bir satır sonu duyurur.

Yapmayın:

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

Yapın:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Yinelenen öznitelikler geçersiz HTML'dir ve tarayıcılar yalnızca ilk geçtiği yeri tutup gerisini sessizce atar; bu yüzden ikinci class ya da style değeri hiçbir zaman etkili olmaz ve bu da gerçek hataları gizler. Denetim şablonlardan haberdardır: birbirini dışlayan dallarda (`{% if %}`/`{% else %}`) tekrarlanan bir öznitelik bildirilmez, çünkü yalnızca bir kopyası işlenebilir.

Yapmayın:

```html
<div class="card" id="profile" class="active">...</div>
```

Yapın:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

Eşleşen bitiş etiketi olmayan `{% if %}`, `{% for %}` ya da `{% macro %}` gibi bir blok etiketi Django ve Jinja'da kesin bir TemplateSyntaxError'dır: sayfa istek sırasında işlenemez; bu kural da bunu dağıtımdan önce yakalar. Kural ayrıca açılış etiketi olmayan, eşi bulunmayan bitiş etiketlerini ve yanlış iç içe geçmiş blokları da (örn. `{% if %}``{% for %}``{% endif %}`) bildirir.

`{% block %}`/`{% endblock %}` eşleşmesi ve endblock adı uyuşmazlıkları bu kural tarafından denetlenir; T003 (varsayılan olarak kapalı) ek olarak çok satırlı her `{% endblock %}` için bir ad ister. custom_blocks ile kaydedilmiş özel blok etiketleri de, kendiliğinden kapanan / %} biçimleri dahil, denetlenir.

Yapmayın:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

Yapın:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

`{{` ya da `{%` ile açılıp eşleşen `}}` ya da `%}` ile hiç kapatılmayan bir şablon etiketi etiket olarak ayrıştırılmaz: Django/Jinja ya bir TemplateSyntaxError fırlatır ya da ham süslü parantez karakterlerini sayfaya basar ve bir sonraki sınırlayıcıya kadar her şey sessizce yutulabilir. Bu yazım hataları (tek bir eksik süslü parantez, uyuşmayan bir sınırlayıcı) incelemede kolayca gözden kaçar, çünkü şablon yine de kısmen işlenebilir.

Yapmayın:

```html
<p>{{ user.name }</p>
```

Yapın:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

Şablon adı eksik, boş ya da yalnızca boşluktan oluşan bir `{% extends %}` ya da `{% include %}` etiketinin yükleyecek hiçbir şeyi yoktur: ad tamamen eksikse Django TemplateSyntaxError, boşsa işleme sırasında TemplateDoesNotExist fırlatır; böylece şablon dosyasının kendisi sözdizimi açısından makul görünse bile sayfa üretimde 500 hatası verir.

Yapmayın:

```html
{% extends "" %}
```

Yapın:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

Bir HTML etiketi bir `{% block %}` içinde açılıp başka bir blokta kapatıldığında, bu bloklardan yalnızca birini geçersiz kılan bir alt şablon öğenin yarısını devralır ve işlenen sayfada dengesiz işaretleme oluşur. Tarayıcılar da öğeleri öngörülemez biçimde otomatik kapatır ya da yeniden iç içe yerleştirir; bu da asıl düzenlenen şablondan çok uzaktaki yerleşimi ve CSS seçicilerini bozar. Her öğeyi aynı blok içinde açıp kapatmak, her bloğun bağımsız olarak güvenle geçersiz kılınabilmesini sağlar.

Yapmayın:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

Yapın:

```html
{% block content %}
<div class="wrapper">
</div>
{% endblock content %}
{% block footer %}
{% endblock footer %}
```

#### T041

`Extends tag should be the first tag in the template.`

Django, `{% extends %}` etiketinden önce başka bir etiketin geldiği şablonu derlemeyi reddeder; ondan önce yazılan metin ise işlenir ve böylece üst şablonun ürettiği her şeyden önce sayfaya sızar. Jinja da bu metni işler, nunjucks ise atar; yani her motorda şablon, göründüğü şeyi yapmaz.

Bir `{# #}` yorumu hiçbir şey üretmez ve sayılmaz; adlandırılmış olsun ya da olmasın bir `{% comment %}`, <code>{&#37; raw %}</code> ya da `{% verbatim %}` bloğunun içindeki hiçbir şey, üç yazımından herhangi biriyle bir `{# djlint:off #}` bölgesi ya da yaml ön bilgisi (front matter) de sayılmaz. Bir html yorumu ise sayılır: motor onu üst şablonun doctype'ından önce sayfaya yazar ve bu kuralın konusu olan sızıntı da budur. Her biri çıktı üreten bir `{% blocktrans %}` bloğu, bir `{% filter %}` bloğu ve bir `<?php ?>` bloğu da sayılır. Yalnızca ilk `{% extends %}` denetlenir; ikincisi kendi başına bir hatadır. jinja ve nunjucks profillerinde ondan önce gelen bir dal etiketi sayılmaz, çünkü jinja bir üst şablon seçmenin yolu olarak `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` yazımını belgeler; django ise şablonun geri kalanını `{% extends %}` içine okur ve ardından `{% endif %}` etiketini reddeder, bu yüzden bu profilde bir dal etiketi sayılır.

handlebars, golang, liquid ve angular profillerinde uygulanmaz.

Yapmayın:

```html
{% load static %}
{% extends "base.html" %}
```

Yapın:

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

Denetim yalnızca sağlıklı biçimde çözümleyebildiği dosyalarda çalışır: dosya, bu dosyanın hiç göstermediği bir id üretebilecek herhangi bir şey içeriyorsa (form bileşeni gibi bir `{{ ... }}` çıktısı, bir `{% include %}` ya da `{% extends %}` veya tanınmayan bir şablon etiketi) kural o dosya için sessiz kalır. Çalıştığı yerde ise bir bildirim, gerçekten bozuk bir ilişkilendirmedir.

Yapmayın:

```html
<label for="email">Email</label>
<input id="username">
```

Yapın:

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

Bir şablon başka bir şablonu genişlettiğinde, neyin çıktı olarak verileceğine üst şablon karar verir ve alt şablon yalnızca üst şablonun bloklarını doldurur. `{% extends %}` etiketinden sonra ve tüm `{% block %}` bloklarının dışında yazılan metin ya da html, işleme sırasında sessizce atılır; böylece kaynakta düzgün görünen bir paragraf sayfaya hiçbir zaman ulaşmaz.

Orada bulunan bir şablon etiketi yine de çalışır; bu yüzden `{% load %}`, `{% set %}` ve bir bloğu saran bir `{% if %}` olduğu gibi bırakılır; `{# #}` ve `{% comment %}` yorumları, html yorumları, <code>{&#37; raw %}</code> ve `{% verbatim %}` blokları ile çıktı olarak verilmek yerine yakalanan bir `{% macro %}`, blok biçimindeki bir `{% set %}`, bir `{% partialdef %}` ya da bir `{% addtoblock %}` gövdesi de öyle. Bir `{% blocktrans %}` metni bildirilir, çünkü `{% blocktrans %}` bir `{% block %}` değildir. Yalnızca extends etiketinden sonraki içerik dikkate alınır ve bu içeriğin her kesintisiz parçası, başlangıcında bir kez bildirilir.

Motor şablon etiketlerini html'den önce okur; bu yüzden bir html yorumunun ya da bir `<pre>` öğesinin içine yazılmış bir `{% extends %}` yine de çalışır ve dosyayı yine de bir alt şablon yapar; birini gerçekten gizleyen yalnızca `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code> ve `{% verbatim %}` yapılarıdır. Bir html yorumunun içindeki metin her durumda hiçbir okuyucuya ulaşmaz ve bildirilmez, ancak oraya yazılan etiketler yine de okunur.

handlebars, golang, liquid ve angular profillerinde uygulanmaz.

Yapmayın:

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

Yapın:

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

`type` özniteliği olmayan bir `<button>` varsayılan olarak `submit` olur; bu yüzden bir betik çalıştırmak için yazılmış bir düğme, çevresindeki formu da gönderir ve sayfa yeniden yüklenir. Türü açıkça yazmak bunu önler.

Yapmayın:

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

Yapın:

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django, Jinja ve Nunjucks'ın üçü de iki bloğa aynı adı veren bir şablonu ayrıştırmayı reddeder; bu yüzden sayfa hiç yüklenmez. Motorlar iki bloğun bir `{% if %}` etiketinin farklı dallarında bulunmasını önemsemez; bu yüzden her blok adı, bloklar yan yana da olsa biri diğerinin içine yerleştirilmiş de olsa, şablonun tamamında benzersiz olmalıdır.

Yalnızca `{% block %}` sayılır: bir `{% blocktrans %}` blok değildir ve bir `{% endblock name %}` yalnızca kapattığı bloğun adını verir. Motorlar `Content` ve `content` adlarını iki ayrı blok olarak ele aldığından adlar yazıldığı gibi karşılaştırılır.

Yalnızca motorun kendisinin hiç ayrıştırmadığı şeyler atlanır: bir şablon yorumu, bir `{% comment %}` bloğu, bir <code>{&#37; raw %}</code> ya da `{% verbatim %}` gövdesi ve bir `djlint:off` bölgesi. Bir html yorumunun, bir `<script>`, `<style>`, `<pre>` ya da `<textarea>` gövdesinin veya bir `{% filter %}` gövdesinin içine yazılmış bir blok yine de sayılır, çünkü motor bunların hepsini okur ve yinelenen ad için yine hata fırlatır.

Bir `{% embed %}` kendi kapsamını açar: içindeki bloklar bu şablonu değil, gömülen şablonu doldurur; bu yüzden aynı kısmi şablonun iki gömmesinin her biri `{% block body %}` yazabilir. Tek bir gömme içinde tekrarlanan bir ad yine de bildirilir.

handlebars, golang, liquid ve angular profillerinde uygulanmaz.

Yapmayın:

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

Yapın:

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

Her satır kendi başına değerlendirilir; bu yüzden html belirtiminin bir `thead` içinde başlık satırının yanına yerleştirdiği `td` hücrelerinden oluşan açıklama satırı bir karışım sayılmaz. Satırı açan boş bir `td`, ilk sütunu boyunca başlıklar bulunan bir tablonun köşe hücresidir; W3C erişilebilirlik eğitiminin istediği işaretleme de budur; bu yüzden atlanır.

Bir `th` ile bir `td` ekran okuyucu için farklı anlamlar taşır ve genellikle farklı css'e sahiptir; bu yüzden bir başlık satırındaki tek bir başıboş hücre veri olarak okunur ve yanındaki sütunlardan farklı biçimlenir. Bu karışım geçerli html'dir; fark edilmesini zorlaştıran da budur.

Yapmayın:

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

Yapın:

```html
<thead>
  <tr>
    <th>Name</th>
    <th>Size</th>
  </tr>
</thead>
```

#### T044

`Output tag holds a statement keyword; use a block tag.`

golang, handlebars ve angular profillerinde uygulanmaz.

Bir çıktı etiketi bir değer yazdırır; `if`, `for`, `url`, `include` ve diğerleri ise bir blok etiketine ait olan deyimlerdir. Django, Jinja ve Nunjucks'ın üçü de `{{ if x }}` yazımını bir sözdizimi hatasıyla reddeder; `{{ endif }}` gibi tek başına bir kapanış anahtar sözcüğü ise hiçbir şey üretmeyen bir değişken olarak okunur ve kapatması amaçlanan blok açık kalır; böylece sayfa ya hiç yüklenmez ya da koşulun gizlemesi gereken şeyi gösterir.

Yalın bir anahtar sözcük sıradan bir değişken adıdır; bu yüzden `{{ url }}`, `{{ url|default:"/" }}` ve `{{ set.name }}` bildirilmez. Yalnızca argüman verilmiş bir anahtar sözcük ile `{{ endif }}` ya da `{{ else }}` gibi tek başına duran bir kapanış ya da dal anahtar sözcüğü bildirilir. `if` ya da `for` gibi bir denetim anahtar sözcüğü bir ifadeye başlayamaz; bu yüzden ondan sonra gelen her şey, bir operatör de olsa, argümandır ve `{{ if -1 > count }}` bildirilir. Diğer adlar değişken ve işlev olarak da kullanılır; onlarda yalnızca tırnaklı bir dize ya da bir sözcük argüman sayılır; bu yüzden bunlardan biriyle başlayan bir ifade olduğu gibi bırakılır: `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}` ve `{{ filter [0] }}` ifadelerinin hiçbiri bildirilmez.

Bir <code>{&#37; raw %}</code> ya da `{% verbatim %}` bloğunun gövdesi şablon sözdizimi değil metindir ve atlanır; adlandırılmış `{% verbatim vueapp %}...{% endverbatim vueapp %}` biçimi de dahil; bu yüzden bu şekilde korunan bir Vue ya da Handlebars `{{ }}` yapısı bildirilmez. `{% trans "Write {{ if x }} instead" %}` örneğinde olduğu gibi bir blok etiketinin tırnaklı argümanının içine yazılmış bir `{{ }}` da motorun yazdırdığı bir metindir ve olduğu gibi bırakılır.

Yapmayın:

```html
{{ if user.is_active }}
```

Yapın:

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

Ekran okuyucu bir iframe'i erişilebilir adıyla duyurur. Ad yoksa çerçevenin url'sini okur ya da hiçbir şey söylemez ve gömülü sayfaya girmeden önce onun ne olduğunu anlamanın bir yolu kalmaz. WCAG bunu 4.1.2 Ad, Rol, Değer başlığı altında ele alır; axe ve html-validate de bu denetimi varsayılan olarak sunar.

Ad `title`, `aria-label` ya da `aria-labelledby` özniteliğinden gelebilir ve üçünden herhangi biri kuralı karşılar. Bir şablon etiketinin yazdığı ad da sayılır; bu yüzden sayfaya göre başlık alan bir çerçeve bildirilmez.

Yapmayın:

```html
<iframe src="/report/"></iframe>
```

Yapın:

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

Bir html yorumu işaretlemeyi tarayıcıdan gizler, şablon motorundan değil. `<!-- {% include "debug.html" %} -->` yine de dosyayı işler ve `<!-- {% if debug %}...{% endif %} -->` Django, Jinja, Nunjucks, Handlebars ve Go'da aynı şekilde yine de değerlendirilir; bu yüzden bu şekilde yorum satırına alınan bir etiket çalışmaya devam eder ve yazdığı her şey yorumun içine düşer ya da `-->` içeriyorsa yorumun dışına taşar. Bir etiketin çalışmasını yalnızca bir şablon yorumu durdurur: Django ve Jinja'da `{# #}`, Handlebars'ta `{{! }}`, Go'da `{{/* */}}`.

Yalnızca bir deyim etiketi bildirilir: onu destekleyen profillerde `{% %}`, bir handlebars section'ı, kapanışı ya da partial'ı ve `{{if}}` ya da `{{end}}` gibi bir Go anahtar sözcüğü. `<!-- built {{ version }} -->` örneğinde olduğu gibi bir yorumun içine yazdırılan bir değer bilinçli bir kullanımdır ve olduğu gibi bırakılır; bir şablon yorumunun, bir `{% comment %}` bloğunun ya da bir raw bloğunun içindeki etiket ile gövdesi adını verdiği tarayıcıya yönelik işaretleme olan Internet Explorer koşullu yorumu `<!--[if IE]> ... <![endif]-->` da öyle.

Yalın bir Go anahtar sözcüğü diğer tüm motorlarda sıradan bir değişken adıdır; bu yüzden `<!-- period {{ start }} to {{ end }} -->` ve `<!-- Template: {{ template }} -->` Django, Jinja, Nunjucks, Handlebars ve Liquid altında değerdir ve yalnızca `--profile golang` altında deyim olarak okunur. `{{ if .X }}` ve `{{ template "footer" . }}` gibi bir Go işleneni taşıyan anahtar sözcük ise başka hiçbir motorun yazdırmadığı bir deyimdir ve her profilde bildirilir. `{%` de aynı şekilde yalnızca motorun onu desteklediği yerde okunur; bu yüzden `--profile handlebars` ve `--profile golang` altında metindir ve `<!-- battery at 50{% charge -->` örneğinde olduğu gibi ardından kapanış süslü parantezi gelmeyen bir açılış, göründüğü gibi düz yazıdır. Koşullu yorum, öyle yazılmış olandır: `<!--[if` ile açılır ve herhangi bir harf büyüklüğündeki `<![endif]-->` ile kapanır; kapatılmadan bırakılan bir koşullu yorum, tarayıcının onu okuduğu gibi sıradan bir yorumdur ve içindeki etiketler bildirilir.

Yapmayın:

```html
<!-- {% include "banner.html" %} -->
```

Yapın:

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

Pozitif bir `tabindex`, bir öğeyi sekme sırasının başına, tabindex'i olmayan her şeyin önüne çeker. Bunlardan tek biri bile klavye kullanıcısı için tüm sayfanın sırasını değiştirir ve sıranın, bir denetim ekleyen her şablonda elle korunması gerekir. WCAG bunu 2.4.3 Odak Sırası altında ele alır.

`0` bir öğeyi sekme sırasına belgenin ona verdiği yerde yerleştirir, `-1` ise onu sekme sırasından çıkarır ama betikten odaklanılabilir bırakır. İkisi de bildirilmez; değeri burada bilinemeyen, bir şablon etiketinin yazdığı bir değer de bildirilmez.

Yapmayın:

```html
<input tabindex="1">
```

Yapın:

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` bir öğeyi erişilebilirlik ağacından çıkarır ama sekme sırasında bırakır; bu yüzden klavye kullanıcısı yine o öğeye gelir ve hiçbir şey duyurulmaz. Dekoratif bir simgeyi gizlemek bu özniteliğin olağan kullanımıdır ve bildirilmez; yalnızca kendi başına odak alan bir öğe bildirilir.

Bir öğe şu durumlarda odaklanılabilir sayılır: bir `button`, `select`, `textarea`, `iframe` ya da `summary` ise, `href` içeren bir `a` ya da `area` ise, gizli olmayan bir `input` ise, `controls` içeren bir `audio` ya da `video` ise veya `contenteditable` ya da `0` veya daha büyük bir `tabindex` taşıyorsa. `disabled` bir denetim ya da `tabindex="-1"` taşıyan bir denetim zaten sekme sırasının dışındadır ve olduğu gibi bırakılır.

Yapmayın:

```html
<button aria-hidden="true">Close</button>
```

Yapın:

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

Yanlış yazılmış bir aria özniteliği hiçbir şey yapmaz. Hiçbir tarayıcı uyarmaz, hiçbir ekran okuyucu bildirmez ve işaretleme erişilebilir kılınmış gibi görünmeye devam eder; bu yüzden `aria-lable` bir şablonda yıllarca durabilir ve adlandırması amaçlanan denetim adsız kalır.

Kuralın bildiği adlar ARIA'nın tanımladığı adlardır. Bir çatının yazdığı bir bağlama düz bir aria adı değildir; bu yüzden `:aria-label`, `v-bind:aria-label` ve `[attr.aria-label]` olduğu gibi bırakılır.

Yapmayın:

```html
<button type="button" aria-lable="Close">x</button>
```

Yapın:

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no` ve 2'nin altındaki bir `maximum-scale`, bir sayfanın telefonda büyütülmesini engeller; bu da birçok kişi için sayfayı okumanın tek yoludur. WCAG, 1.4.4 Metni Yeniden Boyutlandırma altında %200 ister. Tarayıcılar bu kısıtlamayı giderek daha fazla yok sayıyor, ancak etiket, dikkate alındığı her yerde yakınlaştırmayı yine de kapatır.

Ad ve içerik, hangi sırayla yazılmış olursa olsun bulunur.

Yapmayın:

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

Yapın:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>` ve `<tt>`, sunumu css devraldığında kaldırıldı; `<marquee>`, `<blink>`, `<nobr>` ve `<spacer>` ise hiçbir zaman standart olmadı. Html artık bunların hiçbirini tanımlamıyor; bu yüzden bir tarayıcının onları nasıl yerleştireceğini hiçbir şey garanti etmez ve bir stil sayfası onları bir sınıfı hedeflediği gibi hedefleyemez.

Kuralın bildiği öğeler şunlardır: `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt` ve `xmp`. Yalnızca açılış etiketi bildirilir, böylece her öğe bir kez anılır; adı yalnızca bunlardan biriyle başlayan `<font-picker>` gibi özel bir öğe ise olduğu gibi bırakılır.

Yapmayın:

```html
<center><font color="red">Warning</font></center>
```

Yapın:

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

Hiçbir belirtimin adını vermediği bir rol doğrudan atılır ve öğe zaten sahip olduğu anlamı korur; bu yüzden `role="buton"` bir `<div>` öğesini yine bir `<div>` olarak bırakır: işaretleme ona bir amaç verilmiş gibi görünürken ekran okuyucu için hiçbir şey ifade etmez. Bu konuda hiçbir şey uyarmaz; bu yazım hatasını yakalamaya değer kılan da budur.

Kuralın bildiği adlar, ARIA'nın yazarlar için tanımladığı roller ile DPUB-ARIA'nın (`doc-chapter` ve diğerleri) ve GRAPHICS-ARIA'nın (`graphics-symbol` ve diğerleri) eklediği rollerdir. `landmark` ve `sectionhead` gibi ARIA'nın soyut rolleri bildirilir: belirtim, bunların kendi ontolojisini kurmak için var olduğunu ve işaretlemede yazılmaması gerektiğini söyler.

Bir `role`, yedek liste olarak birkaç ad içerebilir ve her biri denetlenir. Şablon sözdizimi içeren bir değer bilinemez ve olduğu gibi bırakılır; `:role` ya da `[attr.role]` örneklerinde olduğu gibi bir çatının yazdığı bir bağlama da öyle.

Yapmayın:

```html
<div role="buton">Save</div>
```

Yapın:

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

Zamanlanmış bir yenileme, sayfayı okuyan kişinin elinden çekip alır. Yavaş okuyan, ekran okuyucu kullanan ya da sadece sözü kesilen biri, hiçbir uyarı ve durdurma yolu olmadan kaldığı yeri kaybeder; bu, WCAG 2.2.1 Ayarlanabilir Zamanlama ölçütünün karşılanmaması demektir. Aynı sayfayı yeniden yükleyen bir yenileme de sayfaya yazılan her şeyi çöpe atar.

Sıfır gecikme bir zamanlayıcı değil, anında bir yönlendirmedir; WCAG buna sunucu yönlendirmesinin kullanılamadığı yerlerde izin verir, bu yüzden bildirilmez. İki öznitelik, hangi sırayla yazılmış olursa olsun bulunur.

Yapmayın:

```html
<meta http-equiv="refresh" content="30">
```

Yapın:

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

Bir id tek bir öğeyi adlandırır. Aynı id'yi taşıyan ikinci bir öğe `getElementById`, `<label for>`, parça bağlantıları ve `aria-labelledby` yapılarını bozar: tarayıcı ilkini alır ve gerisini sessizce yok sayar; böylece bir etiket, bir bağlantı ya da bir betik hiçbir uyarı olmadan yanlış öğeye denk gelir.

Tek bir `{% if %}...{% else %}...{% endif %}` yapısının birbirini dışlayan dallarındaki iki id hiçbir zaman birlikte işlenmez; bu yüzden bildirilmez. Bir `{% for %}` döngüsü ya da bir `{% block %}` dal değildir: bunlardan birinin içindeki bir id ile dışındaki aynı id ikisi de işlenir ve sonraki bildirilir. Bir şablon etiketinin yazdığı bir değer bilinemez ve olduğu gibi bırakılır; boş bir değer de öyle. Id'ler, tarayıcının yaptığı gibi birebir karşılaştırılır; bu yüzden `save` ve `Save` iki ayrı id'dir.

Dallar, dosyanın yazıldığı dilde ve o dilin sınırlayıcılar ile etiket adı arasında izin verdiği her türlü boşlukla okunur: `{% elif %}` ve `{% else %}`, liquid'in `{% elsif %}` ve `{% when %}` etiketleri, go'nun `{{ else }}` etiketi, bir mako `% else:` satır deyimi ve handlebars'ın `{{else}}` etiketi, zincirleme `{{else if x}}` biçimi ve özel yardımcılar dahil herhangi bir `{{#helper}}` bloğunun ters (inverse) bölümü. Bir `<template>` öğesinin içeriği, `getElementById` ile hiçbir zaman erişilemeyen kendine ait bir belge parçasıdır; bu yüzden oradaki bir id yalnızca aynı `<template>` içindeki id'lerle karşılaştırılır: iki şablonun her biri aynı id'ye sahip bir satır içerebilir, ancak tek bir şablonun içindeki iki aynı id yine de bildirilir. Bir yorumun, bir <code>{&#37; raw %}</code> ya da `{% verbatim %}` gövdesinin veya bir `djlint:off` bölgesinin içindeki bir id hiç okunmaz.

Yapmayın:

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

Yapın:

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

Html, `<a>` ve `<button>` içinde etkileşimli içeriği yasaklar. Bir bağlantının içindeki düğme ya da bir düğmenin içindeki bağlantı, tarayıcıların her birinin kendi yöntemiyle onardığı geçersiz bir işaretlemedir ve ekran okuyucu ya da klavye kullanıcısının eline iki denetim gibi davranan tek bir denetim verilir. axe da aynı durumu "nested-interactive" olarak bildirir.

İzlenen kapsayıcılar `href` içeren bir `<a>` ve bir `<button>` öğesidir; bunların içinde bildirilen denetimler ise `href` içeren bir bağlantı, `button`, `input`, `select` ve `textarea` öğeleridir. `href` içermeyen bir `<a>` etkileşimli değildir ve iki tarafta da olduğu gibi bırakılır; gizli bir input ya da türünü bir şablon etiketinin yazdığı bir input da öyle. Bir `<template>` öğesinin içeriği yazıldığı yerde işlenmez; bu yüzden onun içindeki bir denetim çevresindeki bağlantının içine yerleştirilmiş sayılmaz, ancak şablonun içinde yazılmış iç içe yerleştirme yine de bildirilir.

Bir öznitelik, bir etiketin onu yazdığı yerde okunur, başka hiçbir yerde değil: `{% if not href %}` içindeki `href` bir değişkeni adlandırır, `{# href="{{ url }}" #}` içindeki yorum satırına alınmıştır ve `data-attr=href` içindeki başka bir özniteliğe aittir; bir `{% if %}` etiketinin kendi etiketleri arasında yazdığı `href` ise herhangi bir öznitelik gibidir. Açık bırakılan bir bağlantı ya da düğme, bir tarayıcıda olduğu gibi çevresindeki öğeyle birlikte biter; böylece tek bir yazım hatası dosyanın geri kalanının bildirilmesine yol açmaz. En üst düzeyde açık bırakılan birinin ise onu sonlandıracak çevreleyen bir öğesi yoktur ve dosyanın sonuna kadar sürer; orada H025 de eşi olmayan etiketi bildirir.

Yapmayın:

```html
<a href="/cart"><button>Add</button></a>
```

Yapın:

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005, `<html>` üzerinde bir `lang` ister, ancak `lang="english"` ya da `lang="en_US"` gibi bir değer, hiçbir tarayıcının bilmediği bir dili adlandırırken bu kuralı karşılar. Ekran okuyucu bu durumda varsayılan sesine geri döner; çeviri ve heceleme de yanlış kuralları seçer ya da hiçbir kural seçmez. Değer bir BCP 47 etiketi olmalıdır: iki ya da üç harf, ardından her biri bir kısa çizgiden sonra gelen, bir ile sekiz arası harf ya da rakamdan oluşan istenen sayıda alt etiket; `en`, `pt-BR` ya da `zh-Hant-TW` örneklerinde olduğu gibi.

H005 ile uyumlu olarak yalnızca `<html>` etiketi denetlenir. Boş bir değer o kurala bırakılır; yalnızca boşluktan oluşan bir değer ise burada bildirilir, çünkü H005 onu bir değer olarak okur. `lang="{{ LANGUAGE_CODE }}"` örneğinde olduğu gibi bir şablon etiketinin ya da `lang="<?= $lang ?>"` örneğinde olduğu gibi bir php kısa echo'sunun yazdığı bir değer bilinemez ve olduğu gibi bırakılır; ancak `lang="$LANG"` örneğinde olduğu gibi yalnızca `$` ya da `{` ile başlayan bir değer yazıldığı gibi okunur. `xml:lang` ya da `data-lang`, `lang` olarak okunmaz; `{% if a > b %}` örneğinde olduğu gibi öznitelikten önce bir şablon etiketinin içine yazılmış bir `>` da onu gizlemez.

Yapmayın:

```html
<html lang="english">
```

Yapın:

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

Html belirtimi boş bir `src` değerinin geçersiz olduğunu söyler ve tarayıcının onu belgenin kendi url'sine göre çözümlediği konusunda uyarır; bu yüzden `<img src="">` sayfayı yeniden bir görsel olarak, `<script src=""></script>` ise bir betik olarak getirir. Genellikle bir betiğin doldurması amaçlanan bir yer tutucudur ve çözümü, gerçek bir değer olana kadar özniteliği kaldırmak ya da değeri bir data özniteliğinde tutmaktır. `<img src>` örneğinde olduğu gibi hiç değeri olmadan yazılmış bir `src` de boştur ve bildirilir.

Yalnızca `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio` ve `video` denetlenir, çünkü `src` değerinin adlandırdığı şeyi getiren öğeler bunlardır. Yalnızca bir tarayıcının boş olarak okuduğu bir değer bildirilir; bu yüzden `<img src=/static/logo.png>` gibi tırnaksız bir değer, yalnızca boşluktan oluşan bir değer ve bir şablon etiketinin yazdığı bir değer olduğu gibi bırakılır; `srcset` ve `data-src` ise kuralın değerlendirmediği farklı özniteliklerdir.

Yapmayın:

```html
<img src="" alt="Logo">
```

Yapın:

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

Sesli bir video konuşmayı yalnızca ses kanalında taşır; bu yüzden işitme engelli ya da az işiten bir izleyici, WCAG 1.2.2 Altyazılar (Önceden Kaydedilmiş) ölçütünün şart koştuğu altyazılar olmadan videodan hiçbir şey alamaz. `<video>` içinde `kind` değeri `captions` ya da `subtitles` olan bir `<track>` kuralı karşılar; `subtitles` varsayılan olduğundan hiç `kind` içermeyen bir `<track>` da karşılar.

`muted` bir videonun altyazılanacak sesi yoktur ve bildirilmez. Açılış etiketi ya da gövdesi bir şablon etiketi içeren bir video da bildirilmez, çünkü izler ya da `muted` özniteliği djLint'in göremediği yerde şablon tarafından yazılıyor olabilir. Şablon etiketi, bir şablon dilinin açtığı `{{`, `{%`, `{#` ya da `${` yapılarından biri demektir; bu yüzden `onclick="$(this).play()"` gibi bir jQuery işleyicisi, bir Alpine `$refs` ifadesi, bir css süslü parantezi ve yedek metinde yazılmış bir fiyat, göründükleri gibi sıradan metinlerdir ve video yine de okunur.

Yalnızca işaretleme, işaretleme sayılır. `muted` öznitelik olmalıdır; bu yüzden `<video class=muted>` muted adlı bir sınıftır ve bildirilir; yorum satırına alınmış ya da bir öznitelik değerinin içine yazılmış bir `<track>` da iz değil metindir. Bir değerin içindeki `</video>` hiçbir şeyi sonlandırmaz ve öğe, gerçek bitiş etiketinin onu kapattığı yerde değerlendirilir; bu yüzden açık bırakılan bir `<video>` `H025` kuralına bırakılır.

Yapmayın:

```html
<video controls src="talk.mp4"></video>
```

Yapın:

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

<!-- oxfmt-ignore-end -->

### Kural ekleme

Yeni kurallar içeren pull request'leri memnuniyetle karşılıyoruz!

İyi bir kural şunlardan oluşur:

- Ad
- Kod
- Mesaj - Hata bulunduğunda gösterilecek mesaj.
- Bayraklar - Regex bayrakları. Varsayılan değer re.DOTALL'dur. örn: re.I|re.M
- Kalıplar - hatayı bulacak regex ifadeleri.
- Hariç tutma - Kuralın dışarıda bırakılacağı profillerin isteğe bağlı listesi.

Lütfen kuralı doğrulayan bir test de ekleyin.

## Özel kurallar

`pyproject.toml` dosyanızın yanına bir `.djlint_rules.yaml` oluşturarak yalnızca projenize özel kurallar ekleyebilirsiniz. Kurallar bu dosyaya eklenebilir ve djLint onları algılar. Başka bir konumdaki kural dosyası `--rules` CLI seçeneğiyle verilebilir.

### Kalıp kuralları

Regex kalıplarından biri eşleştiğinde başarısız olan kurallar ekleyebilirsiniz:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Python modülü kuralları

Özel bir Python işlevini içe aktarıp çalıştıran kurallar ekleyebilirsiniz:

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

Belirtilen `python_module`, denetlenen her dosyada çalıştırılacak bir `run()` işlevi içermelidir. Bu işlev aşağıdaki argümanları kabul etmelidir:

- `rule`: Kuralınızı `.djlint_rules.yaml` içinde temsil eden dict. Bu değişkeni genellikle kural adına ve mesajına erişmek için kullanırsınız.
- `config`: DJLint yapılandırma nesnesi.
- `html`: Dosyanın tam html içeriği.
- `filepath`: O anda denetlenen dosyanın yolu.
- `line_ends`: Bir karakter konumundan satır numarası elde etmek için `djlint.lint.get_line()` ile kullanabileceğiniz satır `start` ve `end` karakter konumlarının listesi. Örneğe bakın.
- `*args, **kwargs`: İleride başka argümanlar ekleyebiliriz; bu yüzden djLint yükseltmesinde hata riskini azaltmak için bu iki argümanı eklemelisiniz.

Modül proje kökünde olabilir. Bir konum olmayan bir `line` ya da `end` döndürürse djLint, kuralın adını veren bir hatayla durur.

İşlev, her hata için bir tane olmak üzere, aşağıdaki anahtarlara sahip bir dict listesi döndürmelidir:

- `code`: Hatayı bildiren kuralın kod adı (genellikle `rule['name']`)
- `line`: Satır numarası ve bu satırdaki karakter numarası; ':' ile ayrılmış bir dize olarak.
  Örneğin `"2:3"`, hatanın 2. satırın 3. karakterinde bulunduğu anlamına gelir
- `end`: İsteğe bağlı. Hatanın bittiği yer; `line` gibi yazılır ve son karakterinin hemen sonrasını gösterir. Verilmezse hata, `match` değerinin bittiği yerde biter.
- `match`: İçeriğin hatayı içeren kısmı
- `message`: Hatayı bildirmek için yazdırılacak mesaj (genellikle `rule['message']`)

```python
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from djlint.helpers import inside_ignored_linter_block, inside_ignored_rule
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Any

    from djlint.settings import Config
    from djlint.types import LintError


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> list[LintError]:
    """Rule that fails if the html file contains 'bad'.

    This is just an example, in reality it's much simpler to do that with a
    "pattern rule".
    """
    return [
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "end": get_line(match.end(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        }
        for match in re.finditer(r"bad", html)
        if not inside_ignored_rule(config, html, match, rule["name"])
        and not inside_ignored_linter_block(config, html, match)
    ]
```
