---
description: djLint HTML 템플릿 린터의 규칙과 직접 규칙을 추가하는 방법입니다.
title: 린터 규칙
keywords: 템플릿 린터, 템플릿 포맷터, djLint, HTML, 템플릿, 포맷터, 린터, 규칙
---

# 린터 사용법

djLint에는 템플릿의 스타일과 유효성을 검사하는 규칙이 많이 있습니다. 사용하는 템플릿 언어에 맞는 사전 설정 프로필을 쓰도록 구성하면 린터를 최대한 활용할 수 있습니다.

```bash
djlint /path/to/templates --lint

# 사용자 정의 확장자를 쓰는 경우
djlint /path/to/templates -e html.dj --profile=django

# 또는 파일을 지정하는 경우
djlint /path/to/this.html.j2  --profile=jinja
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">모든 옵션은 구성 가이드에서 확인하세요!</a></div>
</div>

## 규칙 켜기와 끄기

대부분의 규칙은 기본으로 켜져 있습니다. 명령줄에서 `--ignore` 플래그로 규칙을 끌 수 있고, `--include` 플래그로 규칙을 켤 수 있습니다.

예시:

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

[{{ "configuration" | i18n }}]({{ "lang_code_url" | i18n }}/docs/configuration) 파일에서도 같은 설정을 할 수 있습니다.

## 규칙

| 코드 | 의미                                                                                       | 기본값 |
| ---- | ------------------------------------------------------------------------------------------ | ------ |
| T001 | 변수는 공백으로 감싸야 합니다. 예: {% raw %}`{{ this }}`{% endraw %}                       | ✔️     |
| T002 | 태그에는 큰따옴표를 사용해야 합니다. 예: {% raw %}`{% extends "this.html" %}`{% endraw %}  | ✔️     |
| T003 | endblock에는 이름이 있어야 합니다. 예: {% raw %}`{% endblock body %}`{% endraw %}.         | -      |
| D004 | (Django) 정적 URL은 {% raw %}`{% static path/to/file %}`{% endraw %} 패턴을 따라야 합니다. | ✔️     |
| J004 | (Jinja) 정적 URL은 {% raw %}`{{ url_for('static'..) }}`{% endraw %} 패턴을 따라야 합니다.  | ✔️     |
| H005 | html 태그에는 비어 있지 않은 `lang` 속성이 있어야 합니다.                                  | ✔️     |
| H006 | `img` 태그에는 `height`와 `width` 속성이 있어야 합니다.                                    | -      |
| H007 | html 태그 앞에 `<!DOCTYPE ... >`가 있어야 합니다.                                          | ✔️     |
| H008 | 속성은 큰따옴표로 감싸야 합니다.                                                           | ✔️     |
| H009 | 태그 이름은 소문자여야 합니다.                                                             | ✔️     |
| H010 | 속성 이름은 소문자여야 합니다.                                                             | ✔️     |
| H011 | 속성 값은 따옴표로 감싸야 합니다.                                                          | ✔️     |
| H012 | 속성의 `=` 주위에 공백이 없어야 합니다.                                                    | ✔️     |
| H013 | `img` 태그에는 alt 속성이 있어야 합니다.                                                   | ✔️     |
| H014 | 빈 줄이 구성에서 유지하는 개수보다 많습니다.                                               | ✔️     |
| H015 | `h` 태그 뒤에는 줄바꿈을 넣어야 합니다.                                                    | ✔️     |
| H016 | html에 `title` 태그가 없습니다.                                                            | ✔️     |
| H017 | 빈 요소 태그는 자체 닫기 형식이어야 합니다(H018과 충돌).                                   | -      |
| D018 | (Django) 내부 링크에는 {% raw %}`{% url ... %}`{% endraw %} 패턴을 사용해야 합니다.        | ✔️     |
| H018 | 빈 요소 태그는 본래 자체적으로 닫히므로 "/>"가 아닌 ">"로 끝나야 합니다(H017과 충돌).      | -      |
| J018 | (Jinja) 내부 링크에는 {% raw %}`{{ url_for() ... }}`{% endraw %} 패턴을 사용해야 합니다.   | ✔️     |
| H019 | `javascript:abc()`를 `on_` 이벤트와 실제 URL로 바꾸세요.                                   | ✔️     |
| H020 | 빈 태그 쌍이 있습니다. 제거를 고려하세요.                                                  | ✔️     |
| H021 | 인라인 스타일은 피해야 합니다.                                                             | ✔️     |
| H022 | 외부 링크에는 HTTPS를 사용하세요.                                                          | ✔️     |
| H023 | 엔티티 참조를 사용하지 마세요.                                                             | ✔️     |
| H024 | script와 style에는 type을 생략하세요.                                                      | ✔️     |
| H025 | 짝이 없는 태그로 보입니다.                                                                 | ✔️     |
| H026 | 비어 있는 id와 class 속성은 제거해도 됩니다.                                               | ✔️     |
| T027 | 템플릿 구문에 닫히지 않은 문자열이 있습니다.                                               | ✔️     |
| T028 | 속성 값 안에서는 공백 제거 태그 사용을 고려하세요. {% raw %}`{%- if/for -%}`{% endraw %}   | -      |
| H029 | form의 method 값에는 소문자 사용을 고려하세요.                                             | ✔️     |
| H030 | meta description 추가를 고려하세요.                                                        | ✔️     |
| T032 | 템플릿 태그에 불필요한 공백이 있습니다.                                                    | ✔️     |
| H033 | form의 action에 불필요한 공백이 있습니다.                                                  | ✔️     |
| T034 | {% raw %}{% ... }% 대신 {% ... %}를 쓰려던 것인가요? {% endraw %}                          | ✔️     |
| H036 | 간격을 띄우려고 `br` 태그를 사용하지 마세요.                                               | ✔️     |
| H037 | 중복된 속성이 있습니다.                                                                    | ✔️     |
| T038 | 블록 태그에 짝이 맞는 끝 태그가 없습니다.                                                  | ✔️     |
| T039 | 닫히지 않은 템플릿 태그가 있습니다.                                                        | ✔️     |
| T040 | extends 또는 include 태그에 템플릿 이름이 없거나 비어 있습니다.                            | ✔️     |
| H041 | 태그를 연 템플릿 블록과 다른 블록에서 태그를 닫았습니다.                                   | ✔️     |
| T041 | extends 태그는 템플릿의 첫 번째 태그여야 합니다.                                           | ✔️     |
| H042 | label의 for 속성과 일치하는 요소 id가 이 파일에 없습니다.                                  | ✔️     |
| T042 | 다른 템플릿을 확장하는 템플릿에서는 블록 밖의 내용이 렌더링되지 않습니다.                  | ✔️     |
| H043 | button 태그에는 `type` 속성이 있어야 합니다.                                               | ✔️     |
| T043 | 템플릿에서 같은 블록 이름이 두 번 이상 쓰였습니다.                                         | ✔️     |
| H044 | thead에 `th` 셀과 `td` 셀을 섞어 쓰면 안 됩니다.                                           | ✔️     |
| T044 | 출력 태그에 문(statement) 키워드가 있습니다. 블록 태그를 사용하세요.                       | ✔️     |
| H045 | iframe 태그에는 `title` 속성이 있어야 합니다.                                              | ✔️     |
| T045 | HTML 주석 안의 템플릿 태그도 실행됩니다. 비활성화하려면 템플릿 주석을 사용하세요.          | ✔️     |
| H046 | tabindex는 양수이면 안 됩니다.                                                             | ✔️     |
| H047 | 포커스를 받을 수 있는 요소에 aria-hidden을 설정하면 안 됩니다.                             | ✔️     |
| H048 | 명세에 정의되지 않은 aria 속성입니다.                                                      | ✔️     |
| H049 | viewport가 페이지 확대를 막으면 안 됩니다.                                                 | ✔️     |
| H050 | 폐기된 요소이므로 다른 것으로 바꿔야 합니다.                                               | ✔️     |
| H051 | ARIA가 마크업용으로 정의한 role이 아닙니다.                                                | ✔️     |
| H052 | meta refresh로 타이머에 따라 페이지를 새로 고치거나 리디렉션하면 안 됩니다.                | ✔️     |
| H053 | 파일에서 같은 id가 두 번 이상 쓰였습니다.                                                  | ✔️     |
| H054 | 대화형 요소를 다른 대화형 요소 안에 중첩하면 안 됩니다.                                    | ✔️     |
| H055 | lang 속성은 en이나 pt-BR 같은 언어 태그여야 합니다.                                        | ✔️     |
| H056 | src는 비어 있으면 안 됩니다.                                                               | ✔️     |
| H057 | video에는 자막 트랙이 있어야 합니다.                                                       | ✔️     |

### 코드 패턴

코드의 첫 글자는 다음 패턴을 따릅니다.

::: content

- D: Django에만 적용
- H: html에 적용
- J: Jinja에만 적용
- M: Handlebars에만 적용
- N: Nunjucks에만 적용
- T: 템플릿 전반에 적용
:::

### 규칙 상세

<!-- oxfmt-ignore-start -->

{% raw %}

#### T001

`Variables should be wrapped in a whitespace.`

`{{user.name}}`처럼 안쪽 여백이 없는 템플릿 구문은 훑어보거나 diff로 비교하기가 더 어렵습니다. 또 코드베이스 전체에서 공백 사용이 일정하지 않으면 같은 표현식이 여러 가지 철자로 존재하게 되어, grep으로 변수나 태그를 찾아 리팩터링하는 작업을 믿을 수 없게 됩니다. Django와 Jinja의 스타일 가이드는 모두 `{{ var }}`와 `{% tag %}`처럼 공백을 한 칸씩 넣어 씁니다.

handlebars와 golang 프로필에는 적용되지 않습니다.

잘못된 예:

```html
{{user.name}}
```

올바른 예:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

템플릿 태그(`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`)에서 작은따옴표와 큰따옴표를 섞어 쓰면 같은 템플릿 이름이 두 가지 철자로 나타나므로, 검색이나 일괄 이름 변경에서 절반을 놓치게 됩니다. 큰따옴표로 통일하면 태그 인수가 파일의 나머지 부분에 있는 HTML 속성의 따옴표와 일관성을 유지합니다.

HTML 속성 값 안의 작은따옴표(예: `<span title="{% trans 'x' %}">`)는 보고하지 않습니다. 속성을 감싼 큰따옴표 때문에 그 안에서는 작은따옴표를 쓸 수밖에 없기 때문입니다.

`quote_style = "single"`을 지정하면 이 규칙은 대신 작은따옴표를 요구하고, 포맷터도 작은따옴표로 씁니다.

`--reformat`이 이 따옴표를 대신 바꿔 줍니다.

잘못된 예:

```html
{% extends 'base.html' %}
```

올바른 예:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

`{% block %}`이 여러 줄에 걸쳐 있거나 블록이 중첩되어 있으면, 이름 없는 `{% endblock %}`만으로는 어느 블록을 닫는지 알 수 없어서 편집하다가 엉뚱한 블록을 닫기 쉽습니다. 그러면 자식 템플릿이 엉뚱한 내용을 재정의하게 됩니다. endblock에 이름을 붙이면 짝이 문서화되고, djLint와 Django(endblock 이름이 맞지 않으면 TemplateSyntaxError를 발생시킵니다) 모두 잘못된 위치에서 닫힌 블록을 잡아낼 수 있습니다. 짝 맞춤 오류(닫히지 않은 블록, 짝 없는 endblock, 일치하지 않는 이름)는 정확성 검사로서 T038이 처리합니다.

기본으로 꺼져 있으며, `--include=T003`으로 켭니다. `--name-endblocks`가 이름을 대신 써 줍니다.

블록이 같은 줄에서 열리고 닫히는 경우에는 이름이 필요하지 않습니다(예: `{% block title %}``{% endblock %}`). 포맷터는 다른 태그를 담은 블록의 내용을 각각 별도의 줄로 옮기므로, 한 줄로 쓴 블록도 포맷한 뒤에는 이름이 필요해질 수 있습니다. `--name-endblocks`를 사용하면 포맷터가 그 이름도 써 줍니다.

잘못된 예:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

올바른 예:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

/static/ 경로를 하드코딩하면 Django의 `{% static %}` 태그를 거치지 않게 됩니다. 그러면 STATIC_URL이 바뀔 때(예: 에셋을 CDN으로 옮기거나 하위 경로에 배포할 때) 템플릿이 깨지고, ManifestStaticFilesStorage가 만드는 해시된 파일 이름도 반영되지 않아 프로덕션에서 404가 나거나 오래된 캐시 에셋이 제공됩니다. 이 규칙은 리터럴 `/static/` 접두사를 찾으므로, 다른 경로에서 정적 파일을 제공하는 프로젝트는 대상이 아닙니다.

잘못된 예:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

올바른 예:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

/static/ 경로를 하드코딩하면 Flask/Jinja의 url_for('static', ...)를 거치지 않게 됩니다. 그러면 앱이 URL 접두사 아래에 마운트되거나 정적 폴더나 호스트가 바뀔 때 에셋이 404가 되고, 프레임워크가 붙여 주는 캐시 무효화용 쿼리 문자열도 사라집니다. 이 규칙은 리터럴 `/static/` 접두사를 찾으므로, 다른 경로에서 정적 파일을 제공하는 프로젝트는 대상이 아닙니다.

잘못된 예:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

올바른 예:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

`<html>`에 lang 속성이 없으면 스크린 리더가 발음 규칙을 추측하므로 페이지를 엉뚱한 언어로 읽을 수 있고, 브라우저도 번역, 하이픈 처리, 로캘에 맞는 인용 부호를 제대로 제공하지 못합니다. 페이지 언어 선언은 WCAG 2.1 성공 기준 3.1.1(수준 A)입니다.

`lang=""`과 값이 없는 `lang`은 모두 언어를 알 수 없다는 뜻이므로, 속성이 없는 경우와 똑같이 보고합니다.

잘못된 예:

```html
<!DOCTYPE html>
<html>
</html>
```

올바른 예:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

기본으로 꺼져 있으며, `--include=H006`으로 켭니다.

`<img>`에 너비와 높이가 없으면 브라우저가 이미지를 내려받기 전에 공간을 확보할 수 없으므로, 이미지가 로드될 때 주변 콘텐츠가 밀려납니다. 이런 레이아웃 이동은 Cumulative Layout Shift(Core Web Vitals 지표)를 악화시키고, 페이지가 자리 잡는 동안 사용자가 잘못 클릭하게 만들 수 있습니다.

잘못된 예:

```html
<img src="cat.png" alt="Cat">
```

올바른 예:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

`<html>` 태그 앞에 `<!DOCTYPE>`이 없으면 브라우저는 페이지를 쿼크 모드로 렌더링해 예전 박스 모델과 레이아웃 동작을 흉내 내므로, 브라우저마다 CSS가 다르게 렌더링됩니다. doctype 앞에 템플릿 태그나 주석이 있는 것은 괜찮습니다. doctype이 `<html>` 태그보다 앞에 있기만 하면 됩니다.

잘못된 예:

```html
<html lang="en">
</html>
```

올바른 예:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

따옴표 스타일이 섞여 있으면 속성 값을 훑어보거나 grep으로 찾기가 어렵고, 작은따옴표로 감싼 값은 내용에 아포스트로피가 들어가는 순간 깨집니다. 큰따옴표는 HTML 명세, 포맷터, 대부분의 스타일 가이드가 따르는 관례이므로, 큰따옴표로 통일하면 템플릿이 더 넓은 생태계와 일관성을 유지합니다.

잘못된 예:

```html
<div class='content'></div>
```

올바른 예:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

HTML 파서는 대문자 태그 이름을 받아들이지만, XHTML과 XML 직렬화는 대소문자를 구분하므로 대문자 태그 이름을 거부합니다. 또 대소문자가 섞여 있으면 텍스트 검색과 diff 리뷰를 믿을 수 없게 됩니다(`<h1>`을 grep하면 `<H1>`을 놓칩니다). 태그 이름을 소문자로 쓰면 템플릿의 이식성과 일관성이 유지됩니다.

포맷터가 대소문자를 그대로 두게 하는 `--ignore-case`를 사용하면 보고하지 않습니다.

잘못된 예:

```html
<H1>Welcome</H1>
```

올바른 예:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

대문자 속성 이름은 XHTML/XML 직렬화에서 유효하지 않으며, 템플릿 전체에서 텍스트 검색을 어렵게 만듭니다(src=를 grep하면 SRC=를 놓칩니다). DOM은 어차피 HTML 속성 이름을 소문자로 정규화하므로, 대문자 표기는 아무런 이점 없이 일관성만 해칩니다. 포맷터가 소문자로 바꾸는 이름인 `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media`, `srcset`만 보고합니다. `--reformat`이 이를 대신 고쳐 주며, `:itemID` 같은 프레임워크 바인딩이나 `data-ID` 같은 더 긴 이름은 대소문자를 그대로 유지합니다.

포맷터가 대소문자를 그대로 두게 하는 `--ignore-case`를 사용하면 보고하지 않습니다.

잘못된 예:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

올바른 예:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

따옴표 없는 속성 값은 첫 번째 공백에서 끝나므로, class=btn primary 같은 값은 공백 뒤의 내용이 모두 조용히 사라집니다(브라우저는 "primary"를 별도의 불리언 속성으로 취급합니다). 템플릿 변수에서 오는 값은 특히 취약해서, 렌더링 결과에 공백, "=", ">"가 하나라도 들어가면 태그가 망가집니다. 따옴표로 감싸면 값의 경계가 명확하고 안전해집니다.

잘못된 예:

```html
<div class=test></div>
```

올바른 예:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

HTML은 "=" 주위의 공백을 허용하므로 이 규칙은 스타일 규칙입니다. name="value"처럼 공백 없이 쓰는 것이 일반적인 스타일이고, grep이나 찾아 바꾸기 같은 단순한 텍스트 도구도 이렇게 붙어 있다고 가정합니다. 그래서 공백이 섞여 있으면 속성을 찾거나 리팩터링하기가 더 어렵습니다. `--reformat`이 공백을 대신 없애 줍니다.

잘못된 예:

```html
<div class = "test"></div>
```

올바른 예:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

alt 속성이 없으면 스크린 리더가 이미지의 파일 이름을 읽거나 아무것도 읽지 않으므로 WCAG 1.1.1(텍스트가 아닌 콘텐츠)을 충족하지 못합니다. alt 텍스트는 이미지를 불러오지 못했을 때 사용자에게 보이는 내용이기도 합니다. 장식용 이미지에는 보조 기술이 건너뛸 수 있도록 명시적으로 빈 alt=""를 지정해야 하며, 이것으로도 이 규칙을 충족합니다.

값이 없는 `alt`는 장식용 이미지의 경우인 `alt=""`와 같으므로 허용합니다.

잘못된 예:

```html
<img src="cat.jpg" height="200" width="300">
```

올바른 예:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

연속된 빈 줄은 렌더링된 페이지에 아무런 영향을 주지 않지만(HTML은 공백을 축약합니다) 템플릿을 부풀리고, 이웃한 줄이 바뀔 때 diff를 지저분하게 만듭니다. djLint의 포맷터는 기본적으로 빈 줄을 모두 제거하므로(빈 줄은 최대 `max_blank_lines`개까지 유지하며 기본값은 0입니다), 연속된 빈 줄이 남아 있다면 포맷되지 않은 코드라는 뜻입니다.

잘못된 예:

```html
<div>one</div>


<p>two</p>
```

올바른 예:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

제목은 문서 개요를 정의하는 블록 수준의 랜드마크입니다. 닫는 h 태그와 같은 줄에 다음 요소를 몰아넣으면 소스에서 그 구조가 가려지고, 둘 중 어느 요소를 편집하든 diff에서는 두 요소가 모두 바뀐 것으로 보입니다. 제목마다 뒤에 줄바꿈을 넣으면 템플릿의 시각적 구조가 렌더링된 개요와 일치합니다.

잘못된 예:

```html
<h1>Heading</h1><p>Intro text.</p>
```

올바른 예:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

HTML 명세는 모든 문서에 title 요소를 요구합니다. title이 없으면 브라우저 탭, 북마크, 방문 기록에 페이지 이름 대신 URL이 그대로 표시되고, 검색 엔진은 페이지의 주요 레이블을 잃으며, 스크린 리더 사용자는 페이지를 열 때 가장 먼저 들려주는 정보를 잃게 되어 WCAG 2.4.2(페이지 제목, 수준 A)를 충족하지 못합니다.

완전한 `<html>`...`</html>` 문서를 담은 파일에서만 보고하므로, 부분 템플릿이나 기본 템플릿을 확장하는 자식 템플릿은 보고하지 않습니다. 클라이언트 측에서 제목을 설정하는 SPA 셸에도 정적인 `<title>`이 필요합니다. 첫 페인트와 크롤러에서, 그리고 JavaScript가 실패했을 때 표시되는 것이 이 제목이기 때문입니다.

잘못된 예:

```html
<html lang="en">
<body>Content</body>
</html>
```

올바른 예:

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

XML/XHTML로도 파싱되어야 하는(또는 XML 기반 도구에 입력되는) 템플릿은 닫는 슬래시 없이 쓴 빈 요소를 거부하며, 코드베이스 전체에서 `<br>`과 `<br />`을 섞어 쓰면 diff가 일관되지 않습니다. 이 규칙은 모든 빈 요소를 같은 방식으로 닫도록 XHTML 스타일 관례를 강제합니다.

기본으로 꺼져 있으며, `--include=H017`로 켭니다. H018과 함께 쓸 수 없으므로 두 관례 중 하나만 켜세요. `--close-void-tags`가 html 빈 요소 태그에 슬래시를 대신 붙여 줍니다. svg `<path>`는 쓴 그대로 두므로 손으로 닫으세요.

잘못된 예:

```html
<br>
<meta charset="utf-8">
```

올바른 예:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

하드코딩한 내부 URL은 urls.py에서 라우트 경로가 바뀌면 조용히 낡아져서, URLconf 테스트로는 잡을 수 없는 깨진 링크와 동작하지 않는 폼 action이 생깁니다. `{% url %}`은 라우트 이름으로 경로를 찾으므로, 경로 이름을 바꾸면 모든 링크가 한꺼번에 업데이트됩니다.

잘못된 예:

```html
<a href="/accounts/login">Login</a>
```

올바른 예:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

HTML 리빙 표준에서 빈 요소 끝의 슬래시는 아무 의미가 없습니다(파서가 무시합니다). 따라서 `<br />`처럼 쓰면 HTML에는 없는 XML 스타일의 자체 닫기 동작이 있는 것처럼 보이고, 읽는 사람이 빈 요소가 아닌 태그에도 슬래시를 붙이도록 오해하게 만들 수 있습니다. 그런 태그에서는 잘못 붙은 /가 조용히 버려져 닫히지 않은 태그 버그를 가립니다. 이 규칙은 빈 요소를 그냥 >로 끝내도록 강제합니다.

기본으로 꺼져 있으며, `--include=H018`로 켭니다. H017과 함께 쓸 수 없으므로 두 관례 중 하나만 켜세요. SVG는 XML이라서 슬래시가 필요하므로 SVG `<path />`는 예외입니다. `--close-void-tags`를 사용하면 이 규칙이 보고하는 슬래시를 포맷터가 쓰게 되므로 보고하지 않습니다.

잘못된 예:

```html
<br />
<meta charset="utf-8" />
```

올바른 예:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

하드코딩한 내부 URL은 라우트 경로가 바뀌거나 앱이 접두사 아래에 마운트되면 조용히 깨져서, 죽은 링크와 404로 전송되는 폼 action을 남깁니다. url_for()는 엔드포인트 이름으로 URL을 만들므로, 라우트가 바뀌면 모든 템플릿에 자동으로 반영됩니다.

잘못된 예:

```html
<a href="/accounts/login">Login</a>
```

올바른 예:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

javascript: URL은 가운데 버튼 클릭과 새 탭에서 열기를 망가뜨리고, JavaScript가 꺼져 있거나 로드에 실패하면 아무 동작도 하지 않으며, 엄격한 콘텐츠 보안 정책(CSP)에 차단되고, 전형적인 XSS 주입 지점이기도 합니다. href에는 실제 URL을 쓰고, 동작은 이벤트 핸들러로 붙이세요. 엄격한 CSP에서는 인라인 on* 핸들러도 차단됩니다. 예시의 onclick은 템플릿 안에서 할 수 있는 최소한의 수정일 뿐이며, 스크립트 파일에서 addEventListener로 리스너를 붙이는 방식이 더 좋습니다.

잘못된 예:

```html
<a href="javascript:openPopup()">Open popup</a>
```

올바른 예:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

빈 태그 쌍은 아무 내용도 렌더링하지 않지만 DOM 노드는 만들어지므로, 스타일시트의 margin, border, flex/grid 간격이 적용되어 추적하기 어려운 유령 간격이 생깁니다. 대개 이전 편집에서 남은 마크업입니다. 일반적인 마크업에서 비어 있어도 정당한 태그(td, th, li, dt, dd, slot)는 예외입니다. 속성이 하나라도 있는 태그(`<div id="app">``</div>` 같은 JS 마운트 지점, `<i class="fa fa-user">``</i>` 같은 아이콘 폰트 요소)도 보고하지 않습니다. 속성이 전혀 없는 빈 쌍만 해당합니다.

잘못된 예:

```html
<p>Saved.</p>
<span> </span>
```

올바른 예:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

인라인 스타일은 어떤 스타일시트 선택자보다도 명시도가 높아서 나중에 재정의하려면 !important가 필요합니다. 또 style-src에 'unsafe-inline'이 없는 콘텐츠 보안 정책에서는 차단되고, 표현이 템플릿 곳곳에 흩어지므로 테마나 디자인을 바꾸려면 스타일시트 하나가 아니라 마크업을 고쳐야 합니다. 선언을 CSS 클래스로 옮기세요. HTML 이메일 템플릿은 정당한 예외입니다. 많은 이메일 클라이언트가 `<style>` 블록을 제거하므로 인라인 스타일이 표준 기법입니다. 이메일 템플릿 디렉터리는 제외하거나 해당 템플릿에서는 이 규칙을 끄세요.

잘못된 예:

```html
<div style="color: red;">Wrong username or password.</div>
```

올바른 예:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

HTTPS로 제공되는 페이지의 http:// 하위 리소스는 혼합 콘텐츠입니다. 브라우저는 스크립트, 스타일시트, iframe을 아예 차단하고, 이미지는 자동으로 업그레이드하거나 경고를 표시합니다. http:// 페이지로 가는 `<a>` 링크는 혼합 콘텐츠는 아니지만, 방문자를 가로채기와 변조에 노출된 암호화되지 않은 연결로 보냅니다. 실제로 TLS가 없는 내부 호스트를 참조하는 경우에도 보고되니, 규칙을 끄기보다는 해당 부분을 `{# djlint:off H022 #}` 블록으로 묶어 보고되지 않게 하세요.

잘못된 예:

```html
<a href="http://example.com">Example</a>
```

올바른 예:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

HTML5 문서는 UTF-8이므로 문자를 그대로 쓰면 어디서나 동작하고, 리뷰어가 실제로 읽는 것도 그 문자입니다. 엔티티 참조에 오타가 있으면(예: `&mdsah;`) 브라우저는 이를 잡아내지 못하고 깨진 텍스트로 그대로 렌더링합니다. djLint는 구문을 담당하는 엔티티(`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;`, 그리고 문자로 쓰면 템플릿 구분자를 완성하게 되는 중괄호 `&lbrace;`, `&rbrace;`와 `&percnt;`, `&num;`, `&dollar;`)와, 보이지 않는 문자라서 문자 그대로는 리뷰할 수 없는 문자를 나타내는 엔티티를 허용합니다. 공백(`&nbsp;`, `&thinsp;`, `&hairsp;`), 결합 문자와 방향 표시(`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`), `&shy;`가 여기에 해당하며, 이름, 10진수, 16진수 형식 모두 마찬가지입니다.

`--reformat`이 엔티티를 문자로 대신 바꿔 줍니다. 템플릿 태그 안에 쓴 엔티티는 페이지가 아니라 태그의 일부이므로 규칙과 포맷터 모두 건드리지 않습니다. `--no-entity-formatting`은 이 변환을 끄지만 규칙은 그대로 두므로, 엔티티는 계속 보고됩니다. 엔티티를 유지하려면 `ignore`에 `H023`을 추가하세요.

잘못된 예:

```html
<p>Dates 1900 &mdash; 2000</p>
```

올바른 예:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript와 text/css는 HTML5에서 `<script>`와 `<style>`의 기본값이므로, 이 속성은 브라우저가 무시하는 군더더기이며 WHATWG 명세도 생략하라고 명시합니다. 이 속성을 빼 두면, 낡은 MIME 문자열이 모듈 스크립트(type="module"이 실제로 의미가 있는 곳)에 복사되어 요소를 망가뜨리는 일도 막을 수 있습니다.

잘못된 예:

```html
<script type="text/javascript" src="app.js">
```

올바른 예:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

여는 태그나 닫는 태그의 짝이 없는 태그가 있으면 브라우저의 오류 복구가 요소의 끝을 추측해야 하므로, 뒤따르는 마크업이 엉뚱한 요소에 흡수됩니다. 그러면 레이아웃, CSS 선택자, JavaScript DOM 쿼리가 조용히, 그리고 브라우저마다 다르게 깨집니다. H025는 `<p>` 안에서 연 `<ol>`이나 `<ul>`도 보고합니다. HTML 파서는 목록 앞에서 단락을 닫으므로, 마크업이 쓴 대로 중첩되지 않기 때문입니다.

잘못된 예:

```html
<div>
  <p>Hello</p>
```

올바른 예:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

빈 속성에 일치하는 class 선택자나 id 선택자는 없으며, 빈 id는 유효하지 않은 HTML입니다(id 값은 빈 문자열이면 안 됩니다). 다만 `div[class]` 같은 속성 존재 선택자는 여전히 일치하므로, 그런 식으로 작성한 스타일시트에서는 속성을 제거한 결과가 드러납니다. 빈 속성은 대개 변수를 넣으려던 템플릿 버그의 신호이므로, 제거하거나 채우면 그런 버그를 놓치지 않습니다.

잘못된 예:

```html
<div id="" class="">content</div>
```

올바른 예:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

`{% ... %}`나 `{{ ... }}` 안에서 연 따옴표를 닫지 않으면 템플릿 엔진이 태그를 잘못 파싱합니다. Django와 Jinja는 렌더링할 때 TemplateSyntaxError를 발생시키거나 태그의 나머지 인수를 조용히 문자열 내용으로 삼켜 버리므로, 페이지가 500 오류를 내거나 인수가 빠진 채로 렌더링됩니다.

잘못된 예:

```html
{% trans "Welcome %}
```

올바른 예:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

기본으로 꺼져 있으며, `--include=T028`로 켭니다.

공백 제거 태그가 없애는 공백은 렌더링되는 공백이므로, 잃을 공백이 없는 속성에만 적용하세요. `alt="{%- if brand -%}Acme{%- endif -%} logo"`는 `Acmelogo`로 렌더링되고, svg의 `d="M12 {%- if big -%}20{%- endif -%} 4Z"`는 다른 경로가 됩니다. 그래서 이 규칙은 직접 켜야 합니다.

속성 값 안의 템플릿 태그는 주변의 공백과 줄바꿈을 렌더링된 속성에 그대로 내보내므로, 일반 `{% if %}`/`{% for %}` 태그로 만든 href나 src에는 불필요한 공백이 섞여 URL이 깨질 수 있습니다. Jinja/Nunjucks의 공백 제어 태그(`{%- ... -%}`)는 주변 공백을 없애 속성이 깔끔한 하나의 값으로 렌더링되게 합니다. class 속성은 클래스 이름 사이에 공백이 더 있어도 문제가 없으므로 예외입니다.

django 프로필에는 적용되지 않습니다. Django 템플릿 태그는 `{%- -%}` 공백 제어를 지원하지 않습니다.

잘못된 예:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

올바른 예:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

HTML 명세는 form의 method 키워드를 소문자(get, post)로 정의하며, 브라우저는 대소문자를 구분하지 않는 대체 매칭으로만 대문자 변형을 받아들입니다. 표준 소문자 형식을 지키면 템플릿이 일관되고 grep으로 찾기 쉬워지며, 엄격한 검사기와 XHTML 기반 도구 체인의 불만도 피할 수 있습니다.

잘못된 예:

```html
<form method="POST"></form>
```

올바른 예:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

검색 엔진은 검색 결과에서 페이지 제목 아래에 표시하는 스니펫으로 meta description을 사용합니다. 이것이 없으면 페이지의 임의 텍스트로 스니펫을 만들어 내므로 클릭률이 떨어지고, 페이지를 공유할 때 링크 미리 보기도 부실해집니다.

완전한 `<html>`...`</html>` 문서를 담은 파일에서만 보고합니다. 스니펫에 관한 이유는 공개적으로 색인되는 페이지에 해당하므로, 인증이 필요한 앱이나 인트라넷 앱에서는 흔히 이 규칙을 끕니다.

잘못된 예:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

올바른 예:

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

템플릿 태그의 인수 사이에 연속된 공백이나 탭은 보이지 않는 잡음입니다. diff에서 실제 차이를 가리고, 빠진 인수를 알아채기 어렵게 만들며, djLint 포맷터가 만드는 공백 한 칸 스타일과 어긋나서 불필요한 재포맷을 일으킵니다. 따옴표로 감싼 문자열 안의 공백은 유지되며 보고하지 않습니다.

잘못된 예:

```html
{% static  'css/style.css' %}
```

올바른 예:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

form의 action 값 앞뒤에 있는 공백은 렌더링된 URL의 일부가 됩니다. 브라우저는 파싱할 때 이를 제거하지만, 브라우저가 아닌 클라이언트나 값을 그대로 사용하는 테스트는 제거하지 않을 수 있습니다. 또 `{% url %}` 태그 주위의 불필요한 공백은 거의 언제나 오타의 신호이며, 이 오타 때문에 렌더링된 제출 URL이 서버 측 라우트 매칭에 실패합니다.

잘못된 예:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

올바른 예:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}%는 거의 언제나 %}의 오타입니다. 템플릿 엔진은 }%를 태그 구분자로 인식하지 않으므로 태그가 파싱되지 않습니다. 그러면 {% ... }% 텍스트가 렌더링된 HTML에 그대로 새어 나가거나, 엔진이 닫히지 않은 태그를 만나 구문 오류를 발생시킵니다.

잘못된 예:

```html
{% include "footer.html" }%
```

올바른 예:

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

HTML 명세는 우편 주소나 시처럼 내용 자체에 속하는 줄바꿈에만 `<br>`을 허용하며, 그런 용도는 보고하지 않습니다. 보고하는 것은 명세가 금지하는 표현 목적의 사용입니다. 즉, 세로 간격을 만드는 두 개 이상의 연속된 줄바꿈과, 블록 요소의 안쪽 가장자리에 붙어서 그 요소의 margin이 할 수 있는 것 외에는 아무것도 렌더링하지 않는 줄바꿈입니다. 둘 다 좁은 화면에서 텍스트 리플로를 망가뜨리고, 스크린 리더는 알릴 것이 없는 곳에서 강제 줄바꿈을 알립니다.

잘못된 예:

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

올바른 예:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

중복 속성은 유효하지 않은 HTML이며, 브라우저는 첫 번째 것만 남기고 나머지는 조용히 버리므로 두 번째 class나 style 값은 적용되지 않고 실제 버그가 가려집니다. 이 검사는 템플릿을 인식합니다. 서로 배타적인 분기(`{% if %}`/`{% else %}`)에서 반복되는 속성은 하나만 렌더링될 수 있으므로 보고하지 않습니다.

잘못된 예:

```html
<div class="card" id="profile" class="active">...</div>
```

올바른 예:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

`{% if %}`, `{% for %}`, `{% macro %}` 같은 블록 태그에 짝이 맞는 끝 태그가 없으면 Django와 Jinja에서는 확실한 TemplateSyntaxError가 됩니다. 요청 시점에 페이지 렌더링이 실패하는데, 이 규칙은 배포 전에 이를 잡아냅니다. 여는 태그가 없는 짝 없는 끝 태그와, 잘못 엇갈린 블록(예: `{% if %}``{% for %}``{% endif %}`)도 보고합니다.

`{% block %}`/`{% endblock %}`의 짝 맞춤과 endblock 이름 불일치는 이 규칙이 검사합니다. T003(기본으로 꺼짐)은 여기에 더해 여러 줄에 걸친 모든 `{% endblock %}`에 이름을 요구합니다. custom_blocks로 등록한 사용자 정의 블록 태그도 검사하며, 자체 닫기 형식인 / %}도 포함됩니다.

잘못된 예:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

올바른 예:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

`{{`나 `{%`로 열었지만 짝이 맞는 `}}`나 `%}`로 닫지 않은 템플릿 태그는 태그로 파싱되지 않습니다. Django/Jinja는 TemplateSyntaxError를 발생시키거나 중괄호 문자를 그대로 페이지에 렌더링하며, 다음 구분자까지의 모든 내용이 조용히 삼켜질 수 있습니다. 이런 오타(중괄호 하나 누락, 구분자 불일치)는 템플릿이 부분적으로는 렌더링될 수 있어서 리뷰에서 놓치기 쉽습니다.

잘못된 예:

```html
<p>{{ user.name }</p>
```

올바른 예:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

템플릿 이름이 없거나, 비어 있거나, 공백뿐인 `{% extends %}`나 `{% include %}` 태그는 불러올 것이 없습니다. Django는 이름이 아예 없으면 TemplateSyntaxError를, 이름이 비어 있으면 렌더링할 때 TemplateDoesNotExist를 발생시키므로, 템플릿 파일 자체는 구문상 그럴듯해 보여도 프로덕션에서 페이지가 500 오류를 냅니다.

잘못된 예:

```html
{% extends "" %}
```

올바른 예:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

HTML 태그를 한 `{% block %}`에서 열고 다른 블록에서 닫으면, 둘 중 한 블록만 재정의하는 자식 템플릿은 요소의 절반만 물려받아 렌더링된 페이지의 마크업 균형이 깨집니다. 그러면 브라우저가 예측할 수 없게 요소를 자동으로 닫거나 다시 중첩해서, 실제로 편집한 템플릿과 멀리 떨어진 곳의 레이아웃과 CSS 선택자가 망가집니다. 각 요소를 같은 블록 안에서 열고 닫으면 모든 블록을 독립적으로 안전하게 재정의할 수 있습니다.

잘못된 예:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

올바른 예:

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

Django는 `{% extends %}` 앞에 다른 태그가 있는 템플릿을 컴파일하지 않으며, 그 앞에 쓴 텍스트는 렌더링되므로 부모 템플릿이 만드는 모든 것보다 앞서 페이지에 새어 나갑니다. Jinja도 그 텍스트를 렌더링하고 nunjucks는 버리므로, 어느 엔진에서든 템플릿이 보이는 대로 동작하지 않습니다.

`{# #}` 주석은 아무것도 렌더링하지 않으므로 세지 않으며, 이름이 있든 없든 `{% comment %}`, <code>{&#37; raw %}</code>, `{% verbatim %}` 블록 안의 내용, 세 가지 표기 중 어느 것으로 쓴 `{# djlint:off #}` 영역, yaml 프런트 매터도 세지 않습니다. HTML 주석은 셉니다. 엔진이 이를 부모 템플릿의 doctype보다 앞서 페이지에 쓰는데, 이 규칙이 잡아내는 누출이 이것입니다. `{% blocktrans %}` 블록, `{% filter %}` 블록, `<?php ?>` 블록도 각각 렌더링되므로 셉니다. 첫 번째 `{% extends %}`만 검사합니다. 두 번째 extends는 그 자체로 오류입니다. jinja와 nunjucks 프로필에서는 그 앞의 분기 태그를 세지 않습니다. jinja는 부모를 선택하는 방법으로 `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}`를 문서화하고 있기 때문입니다. django는 템플릿의 나머지 부분을 `{% extends %}`로 읽어 들인 뒤 `{% endif %}`를 거부하므로, django 프로필에서는 분기 태그도 셉니다.

handlebars, golang, liquid, angular 프로필에는 적용되지 않습니다.

잘못된 예:

```html
{% load static %}
{% extends "base.html" %}
```

올바른 예:

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

이 검사는 확실하게 분석할 수 있는 파일에서만 실행됩니다. 이 파일에 보이지 않는 id를 렌더링할 수 있는 무언가(폼 위젯 같은 `{{ ... }}` 출력, `{% include %}`나 `{% extends %}`, 인식되지 않는 템플릿 태그)가 파일에 있으면 그 파일에서는 보고하지 않습니다. 검사가 실행되는 곳에서 보고된 문제는 실제로 연결이 끊어진 것입니다.

잘못된 예:

```html
<label for="email">Email</label>
<input id="username">
```

올바른 예:

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

템플릿이 다른 템플릿을 확장하면 출력할 내용은 부모가 결정하고, 자식은 부모의 블록을 채우기만 합니다. `{% extends %}` 뒤, 그리고 모든 `{% block %}` 밖에 쓴 텍스트나 HTML은 렌더링할 때 조용히 버려지므로, 소스에서 멀쩡해 보이는 단락이 페이지에는 나타나지 않습니다.

그 위치의 템플릿 태그는 여전히 실행되므로 `{% load %}`, `{% set %}`, 블록을 감싼 `{% if %}`는 보고하지 않습니다. `{# #}`와 `{% comment %}` 주석, HTML 주석, <code>{&#37; raw %}</code>와 `{% verbatim %}` 블록, 그리고 `{% macro %}`, 블록 형식의 `{% set %}`, `{% partialdef %}`, `{% addtoblock %}`의 본문도 출력되지 않고 캡처되므로 보고하지 않습니다. `{% blocktrans %}`의 텍스트는 보고합니다. `{% blocktrans %}`는 `{% block %}`이 아니기 때문입니다. extends 태그 뒤의 내용만 고려하며, 연속된 내용은 각각 시작 위치에서 한 번씩 보고합니다.

엔진은 HTML보다 템플릿 태그를 먼저 읽으므로, HTML 주석이나 `<pre>` 안에 쓴 `{% extends %}`도 여전히 실행되어 파일을 자식 템플릿으로 만듭니다. 이를 실제로 숨기는 것은 `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code>, `{% verbatim %}`뿐입니다. HTML 주석 안의 텍스트는 어느 쪽이든 독자에게 닿지 않으므로 보고하지 않지만, 거기에 쓴 태그는 여전히 읽힙니다.

handlebars, golang, liquid, angular 프로필에는 적용되지 않습니다.

잘못된 예:

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

올바른 예:

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

`type`이 없는 `<button>`은 기본값이 `submit`이므로, 스크립트를 실행하려고 만든 버튼이 주변의 폼까지 제출해서 페이지가 새로 고쳐집니다. type을 명시하면 이를 막을 수 있습니다.

잘못된 예:

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

올바른 예:

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django, Jinja, Nunjucks는 모두 같은 이름의 블록이 두 개 있는 템플릿을 파싱하지 않으므로, 페이지가 아예 로드되지 않습니다. 엔진은 두 블록이 `{% if %}`의 서로 다른 분기에 있어도 신경 쓰지 않으므로, 블록이 나란히 있든 하나가 다른 하나 안에 중첩되어 있든 블록 이름은 템플릿 전체에서 고유해야 합니다.

`{% block %}`만 셉니다. `{% blocktrans %}`는 블록이 아니며, `{% endblock name %}`은 자신이 닫는 블록의 이름을 적을 뿐입니다. 엔진은 `Content`와 `content`를 서로 다른 블록으로 취급하므로, 이름은 쓴 그대로 비교합니다.

엔진 자체가 파싱하지 않는 부분만 건너뜁니다. 템플릿 주석, `{% comment %}` 블록, <code>{&#37; raw %}</code>나 `{% verbatim %}` 본문, `djlint:off` 영역이 여기에 해당합니다. HTML 주석, `<script>`, `<style>`, `<pre>`, `<textarea>` 본문, `{% filter %}` 본문 안에 쓴 블록은 엔진이 모두 읽고 똑같이 중복 이름 오류를 발생시키므로 여전히 셉니다.

`{% embed %}`는 자체 범위를 엽니다. 그 안의 블록은 이 템플릿이 아니라 포함된 템플릿을 채우므로, 같은 부분 템플릿을 두 번 embed하면 각각 `{% block body %}`를 쓸 수 있습니다. 하나의 embed 안에서 반복되는 이름은 여전히 보고합니다.

handlebars, golang, liquid, angular 프로필에는 적용되지 않습니다.

잘못된 예:

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

올바른 예:

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

행은 각각 따로 판단하므로, HTML 명세가 `thead` 안에서 제목 행 옆에 두는 `td`로 된 설명 행은 섞어 쓴 것이 아닙니다. 행 맨 앞의 빈 `td`는 첫 번째 열을 따라 제목이 있는 표의 모서리 셀이며, W3C 접근성 튜토리얼이 요구하는 마크업이므로 건너뜁니다.

`th`와 `td`는 스크린 리더에 서로 다른 의미를 전달하고 보통 CSS도 다르므로, 제목 행에 섞인 셀 하나는 데이터로 읽히고 옆 열과 다르게 스타일이 지정됩니다. 이렇게 섞어 써도 유효한 HTML이라서 알아채기 어렵습니다.

잘못된 예:

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

올바른 예:

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

golang, handlebars, angular 프로필에는 적용되지 않습니다.

출력 태그는 값을 출력하는 태그이며, `if`, `for`, `url`, `include` 같은 키워드는 블록 태그에 들어가야 하는 문(statement)입니다. Django, Jinja, Nunjucks는 모두 `{{ if x }}`를 구문 오류로 거부합니다. 또 `{{ endif }}`처럼 닫는 키워드만 단독으로 쓰면 아무것도 렌더링하지 않는 변수로 읽히고, 닫으려던 블록은 열린 채로 남습니다. 그래서 페이지가 아예 로드되지 않거나, 조건으로 숨겼어야 할 내용이 표시됩니다.

키워드만 단독으로 쓰면 평범한 변수 이름이므로 `{{ url }}`, `{{ url|default:"/" }}`, `{{ set.name }}`은 보고하지 않습니다. 인수가 주어진 키워드와, `{{ endif }}`나 `{{ else }}`처럼 단독으로 쓴 닫는 키워드나 분기 키워드만 보고합니다. `if`나 `for` 같은 제어 키워드는 표현식의 시작이 될 수 없으므로 그 뒤에 오는 것은 연산자를 포함해 모두 인수이며, 따라서 `{{ if -1 > count }}`는 보고합니다. 나머지 이름은 변수나 함수로도 쓰이므로 따옴표로 감싼 문자열이나 단어만 인수로 간주하며, 그래서 우연히 그런 이름으로 시작하는 표현식은 보고하지 않습니다. `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}`, `{{ filter [0] }}`은 모두 보고하지 않습니다.

<code>{&#37; raw %}</code>나 `{% verbatim %}` 블록의 본문은 템플릿 구문이 아니라 텍스트이므로 건너뜁니다. 이름이 있는 형식인 `{% verbatim vueapp %}...{% endverbatim vueapp %}`도 마찬가지이므로, 이런 식으로 보호한 Vue나 Handlebars의 `{{ }}`는 보고하지 않습니다. `{% trans "Write {{ if x }} instead" %}`처럼 블록 태그의 따옴표로 감싼 인수 안에 쓴 `{{ }}`도 엔진이 출력하는 텍스트이므로 보고하지 않습니다.

잘못된 예:

```html
{{ if user.is_active }}
```

올바른 예:

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

스크린 리더는 iframe을 접근 가능한 이름으로 알립니다. 이름이 없으면 프레임의 URL을 읽거나 아무것도 읽지 않으므로, 들어가 보기 전에는 포함된 페이지가 무엇인지 알 방법이 없습니다. WCAG는 이를 4.1.2 이름, 역할, 값에서 다루며, axe와 html-validate 모두 이 검사를 기본으로 제공합니다.

이름은 `title`, `aria-label`, `aria-labelledby`에서 가져올 수 있으며, 셋 중 하나만 있으면 규칙을 충족합니다. 템플릿 태그로 쓴 이름도 인정하므로, 페이지마다 제목을 붙인 프레임은 보고하지 않습니다.

잘못된 예:

```html
<iframe src="/report/"></iframe>
```

올바른 예:

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

HTML 주석은 마크업을 브라우저에게서 숨길 뿐, 템플릿 엔진에게서는 숨기지 않습니다. Django, Jinja, Nunjucks, Handlebars, Go 모두에서 `<!-- {% include "debug.html" %} -->`는 여전히 파일을 렌더링하고 `<!-- {% if debug %}...{% endif %} -->`는 여전히 평가됩니다. 그래서 이런 식으로 주석 처리한 태그는 계속 실행되며, 태그가 출력하는 내용은 주석 안에 들어가거나, 그 내용에 `-->`가 있으면 주석 밖으로 빠져나갑니다. 태그 실행을 막는 것은 템플릿 주석뿐입니다. Django와 Jinja에서는 `{# #}`, Handlebars에서는 `{{! }}`, Go에서는 `{{/* */}}`입니다.

문 태그만 보고합니다. 즉, 이를 지원하는 프로필에서의 `{% %}`, handlebars의 섹션, 닫는 태그, 파셜, 그리고 `{{if}}`나 `{{end}}` 같은 Go 키워드입니다. `<!-- built {{ version }} -->`처럼 주석에 값을 출력하는 것은 의도적인 사용이므로 보고하지 않습니다. 템플릿 주석, `{% comment %}` 블록, raw 블록 안의 태그와, Internet Explorer용 조건부 주석 `<!--[if IE]> ... <![endif]-->`도 보고하지 않습니다. 조건부 주석의 본문은 지정한 브라우저를 위한 마크업이기 때문입니다.

Go 키워드만 단독으로 쓰면 다른 모든 엔진에서는 평범한 변수 이름입니다. 그래서 `<!-- period {{ start }} to {{ end }} -->`와 `<!-- Template: {{ template }} -->`는 Django, Jinja, Nunjucks, Handlebars, Liquid에서는 값이며, `--profile golang`에서만 문으로 읽습니다. `{{ if .X }}`와 `{{ template "footer" . }}`처럼 Go 피연산자가 있는 키워드는 다른 어떤 엔진도 출력하지 않는 문이므로 어느 프로필에서든 보고합니다. 마찬가지로 `{%`도 엔진이 지원하는 곳에서만 읽으므로, `--profile handlebars`와 `--profile golang`에서는 텍스트입니다. 또 `<!-- battery at 50{% charge -->`처럼 뒤에 닫는 중괄호가 없는 여는 구분자는 보이는 그대로 일반 텍스트입니다. 조건부 주석은 그렇게 작성된 것, 즉 `<!--[if`로 시작하고 대소문자에 관계없이 `<![endif]-->`로 닫힌 것만 해당합니다. 닫히지 않은 것은 브라우저가 읽는 대로 일반 주석이며, 그 안의 태그는 보고합니다.

잘못된 예:

```html
<!-- {% include "banner.html" %} -->
```

올바른 예:

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

양수 `tabindex`는 요소를 탭 순서의 맨 앞으로, tabindex가 없는 모든 요소보다 앞으로 끌어옵니다. 이런 요소가 하나만 있어도 키보드 사용자에게는 페이지 전체의 순서가 바뀌며, 그 뒤로는 컨트롤을 추가하는 모든 템플릿에서 순서를 손으로 관리해야 합니다. WCAG는 이를 2.4.3 포커스 순서에서 다룹니다.

`0`은 문서상의 위치에 따라 요소를 탭 순서에 넣고, `-1`은 요소를 탭 순서에서 빼되 스크립트로는 포커스할 수 있게 둡니다. 둘 다 보고하지 않으며, 숫자를 여기서 알 수 없는 템플릿 태그로 쓴 값도 보고하지 않습니다.

잘못된 예:

```html
<input tabindex="1">
```

올바른 예:

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"`는 요소를 접근성 트리에서 빼지만 탭 순서에는 남겨 두므로, 키보드 사용자는 여전히 그 요소에 도달하는데 아무것도 들리지 않습니다. 장식용 아이콘을 숨기는 것은 이 속성의 일반적인 용도이므로 보고하지 않습니다. 스스로 포커스를 받는 요소만 보고합니다.

다음 요소를 포커스를 받을 수 있는 요소로 봅니다. `button`, `select`, `textarea`, `iframe`, `summary`, `href`가 있는 `a`나 `area`, hidden이 아닌 `input`, `controls`가 있는 `audio`나 `video`, 그리고 `contenteditable`이나 `0` 이상의 `tabindex`가 있는 모든 요소입니다. `disabled` 컨트롤이나 `tabindex="-1"`이 있는 컨트롤은 이미 탭 순서에서 빠져 있으므로 보고하지 않습니다.

잘못된 예:

```html
<button aria-hidden="true">Close</button>
```

올바른 예:

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

철자가 틀린 aria 속성은 아무 효과도 없습니다. 브라우저도 경고하지 않고 스크린 리더도 알려 주지 않으며, 마크업은 접근성을 갖춘 것처럼 보입니다. 그래서 `aria-lable`이 템플릿에 몇 년씩 남아 있는 동안, 이름을 붙이려던 컨트롤은 이름 없는 채로 남게 됩니다.

규칙이 아는 이름은 ARIA가 정의한 이름입니다. 프레임워크가 쓰는 바인딩은 평범한 aria 이름이 아니므로 `:aria-label`, `v-bind:aria-label`, `[attr.aria-label]`은 보고하지 않습니다.

잘못된 예:

```html
<button type="button" aria-lable="Close">x</button>
```

올바른 예:

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no`와 2 미만의 `maximum-scale`은 휴대폰에서 페이지를 확대하지 못하게 막습니다. 많은 사람에게는 확대가 페이지를 읽을 수 있는 유일한 방법입니다. WCAG는 1.4.4 텍스트 크기 조정에서 200%를 요구합니다. 브라우저는 점점 이 제한을 무시하는 추세이지만, 제한이 지켜지는 곳에서는 여전히 이 태그가 확대를 끕니다.

name과 content는 어떤 순서로 쓰든 찾아냅니다.

잘못된 예:

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

올바른 예:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>`, `<tt>`는 CSS가 표현을 맡게 되면서 제외되었고, `<marquee>`, `<blink>`, `<nobr>`, `<spacer>`는 애초에 표준이었던 적이 없습니다. 이제 HTML은 이 중 어느 것도 정의하지 않으므로 브라우저가 이를 어떻게 배치할지 보장할 수 없고, 스타일시트도 클래스를 대상으로 하듯 이들을 대상으로 지정할 수 없습니다.

규칙이 아는 요소는 `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt`, `xmp`입니다. 여는 태그만 보고하므로 요소마다 한 번씩만 지적하며, `<font-picker>`처럼 이름이 이 중 하나로 시작할 뿐인 사용자 정의 요소는 보고하지 않습니다.

잘못된 예:

```html
<center><font color="red">Warning</font></center>
```

올바른 예:

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

어떤 명세에도 없는 role은 그냥 버려지고 요소는 원래 의미를 그대로 유지합니다. 그래서 `role="buton"`을 쓴 `<div>`는 그대로 `<div>`입니다. 스크린 리더에게는 아무 의미도 없지만, 마크업은 목적이 부여된 것처럼 보입니다. 아무도 경고해 주지 않기 때문에 이런 오타는 잡아낼 가치가 있습니다.

규칙이 아는 이름은 ARIA가 작성자용으로 정의한 role과, DPUB-ARIA(`doc-chapter` 등)와 GRAPHICS-ARIA(`graphics-symbol` 등)가 추가한 role입니다. `landmark`나 `sectionhead` 같은 ARIA의 추상 role은 보고합니다. 명세에 따르면 추상 role은 온톨로지를 구성하기 위해 존재하며 마크업에 쓰면 안 됩니다.

`role`에는 대체 목록으로 이름을 여러 개 넣을 수 있으며, 각각을 검사합니다. 템플릿 구문이 들어 있는 값은 알 수 없으므로 보고하지 않으며, `:role`이나 `[attr.role]`처럼 프레임워크가 쓰는 바인딩도 보고하지 않습니다.

잘못된 예:

```html
<div role="buton">Save</div>
```

올바른 예:

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

일정 시간 뒤에 새로 고치는 페이지는 읽고 있는 사람 앞에서 페이지를 바꿔 버립니다. 천천히 읽는 사람, 스크린 리더를 쓰는 사람, 잠시 다른 일을 하던 사람은 경고도 없이, 멈출 방법도 없이 읽던 위치를 잃습니다. 이는 WCAG 2.2.1 시간 조절 가능을 충족하지 못하는 것이며, 같은 페이지를 다시 불러오는 새로 고침은 입력해 둔 내용까지 모두 날려 버립니다.

지연 시간이 0이면 타이머가 아니라 즉시 리디렉션이며, WCAG는 서버 리디렉션을 쓸 수 없는 경우에 이를 허용하므로 보고하지 않습니다. 두 속성은 어떤 순서로 쓰든 찾아냅니다.

잘못된 예:

```html
<meta http-equiv="refresh" content="30">
```

올바른 예:

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

id는 요소 하나를 가리킵니다. 같은 id를 가진 두 번째 요소가 있으면 `getElementById`, `<label for>`, 프래그먼트 링크, `aria-labelledby`가 망가집니다. 브라우저는 첫 번째 요소를 선택하고 나머지는 조용히 무시하므로, 레이블, 링크, 스크립트가 아무 경고 없이 엉뚱한 요소를 가리키게 됩니다.

하나의 `{% if %}...{% else %}...{% endif %}`에서 서로 배타적인 분기에 있는 두 id는 동시에 렌더링되지 않으므로 보고하지 않습니다. `{% for %}` 루프나 `{% block %}`은 분기가 아닙니다. 그 안의 id와 밖의 같은 id는 모두 렌더링되므로, 뒤에 오는 쪽을 보고합니다. 템플릿 태그로 쓴 값은 알 수 없으므로 보고하지 않으며, 빈 값도 보고하지 않습니다. id는 브라우저와 마찬가지로 정확히 비교하므로 `save`와 `Save`는 서로 다른 id입니다.

분기는 파일을 작성한 언어에 맞게, 그리고 그 언어가 구분자와 태그 이름 사이에 허용하는 공백이 어떻든 읽어 냅니다. `{% elif %}`와 `{% else %}`, liquid의 `{% elsif %}`와 `{% when %}`, go의 `{{ else }}`, mako의 `% else:` 줄 문, handlebars의 `{{else}}`, 연결된 `{{else if x}}`, 사용자 정의 헬퍼를 포함한 모든 `{{#helper}}` 블록의 역(inverse) 섹션이 해당합니다. `<template>`의 내용은 `getElementById`가 닿지 않는 별도의 문서 조각이므로, 그 안의 id는 같은 `<template>` 안의 id하고만 비교합니다. 두 템플릿이 각각 같은 id의 행을 가질 수는 있지만, 한 템플릿 안에 같은 id가 두 개 있으면 여전히 보고합니다. 주석, <code>{&#37; raw %}</code>나 `{% verbatim %}` 본문, `djlint:off` 영역 안의 id는 아예 읽지 않습니다.

잘못된 예:

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

올바른 예:

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

HTML은 `<a>`와 `<button>` 안에 대화형 콘텐츠를 넣는 것을 금지합니다. 링크 안의 버튼이나 버튼 안의 링크는 유효하지 않은 마크업이며, 브라우저마다 제각기 다른 방식으로 고칩니다. 스크린 리더 사용자나 키보드 사용자에게는 두 개처럼 동작하는 컨트롤 하나가 주어집니다. axe도 같은 문제를 "nested-interactive"로 보고합니다.

감시하는 컨테이너는 `href`가 있는 `<a>`와 `<button>`이며, 그 안에서 보고하는 컨트롤은 `href`가 있는 링크, `button`, `input`, `select`, `textarea`입니다. `href`가 없는 `<a>`는 대화형이 아니므로 어느 쪽에 있든 보고하지 않으며, hidden input이나 템플릿 태그로 type을 쓰는 input도 마찬가지입니다. `<template>`의 내용은 작성한 위치에서 렌더링되지 않으므로, 그 안의 컨트롤은 주변의 링크 안에 중첩된 것이 아닙니다. 다만 템플릿 안에서 작성한 중첩은 여전히 보고합니다.

속성은 태그가 속성을 쓰는 위치에서만 읽습니다. `{% if not href %}`의 `href`는 변수 이름이고, `{# href="{{ url }}" #}`의 것은 주석 처리되었으며, `data-attr=href`의 것은 다른 속성에 속합니다. 반면 `{% if %}`가 자신의 태그 사이에 쓰는 `href`는 다른 속성과 똑같은 속성입니다. 열린 채로 남은 링크나 버튼은 브라우저에서처럼 그것을 감싼 요소와 함께 끝나므로, 오타 하나 때문에 파일의 나머지 부분이 모두 보고되지는 않습니다. 최상위에서 열린 채로 남은 것은 끝낼 감싸는 요소가 없으므로 파일 끝까지 이어지며, 이때 H025도 짝 없는 태그를 보고합니다.

잘못된 예:

```html
<a href="/cart"><button>Add</button></a>
```

올바른 예:

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005는 `<html>`에 `lang`을 요구하지만, `lang="english"`나 `lang="en_US"` 같은 값은 브라우저가 아는 어떤 언어도 가리키지 않으면서 H005를 충족합니다. 그러면 스크린 리더는 기본 음성으로 되돌아가고, 번역과 하이픈 처리는 엉뚱한 규칙을 고르거나 아무 규칙도 고르지 못합니다. 값은 BCP 47 태그여야 합니다. 즉, 두세 글자 뒤에 각각 하이픈으로 시작하는 1~8자의 문자나 숫자로 된 하위 태그가 몇 개든 이어지는 형식으로, `en`, `pt-BR`, `zh-Hant-TW`와 같습니다.

H005와 마찬가지로 `<html>` 태그만 검사합니다. 빈 값은 H005에 맡기며, 공백뿐인 값은 H005가 값으로 읽으므로 여기서 보고합니다. `lang="{{ LANGUAGE_CODE }}"`처럼 템플릿 태그로 쓴 값이나 `lang="<?= $lang ?>"`처럼 PHP 짧은 echo로 쓴 값은 알 수 없으므로 보고하지 않지만, `lang="$LANG"`처럼 `$`나 `{`로 시작할 뿐인 값은 쓴 그대로 읽습니다. `xml:lang`이나 `data-lang`은 `lang`으로 읽지 않으며, `{% if a > b %}`처럼 속성 앞의 템플릿 태그 안에 쓴 `>`가 속성을 가리지도 않습니다.

잘못된 예:

```html
<html lang="english">
```

올바른 예:

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

HTML 명세는 빈 `src`가 유효하지 않다고 정하고, 브라우저가 이를 문서 자체의 URL로 해석한다고 경고합니다. 그래서 `<img src="">`는 페이지를 이미지로 다시 가져오고, `<script src=""></script>`는 페이지를 스크립트로 가져옵니다. 대개 스크립트가 나중에 채우려던 자리 표시자이며, 실제 값이 생길 때까지 속성을 빼거나 값을 data 속성에 담아 두면 해결됩니다. `<img src>`처럼 값 없이 쓴 `src`도 비어 있는 것이므로 보고합니다.

`src`가 가리키는 것을 가져오는 요소인 `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio`, `video`만 검사합니다. 브라우저가 빈 값으로 읽는 값만 보고하므로, `<img src=/static/logo.png>` 같은 따옴표 없는 값, 공백뿐인 값, 템플릿 태그로 쓴 값은 보고하지 않습니다. `srcset`과 `data-src`는 이 규칙이 판단하지 않는 별개의 속성입니다.

잘못된 예:

```html
<img src="" alt="Logo">
```

올바른 예:

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

소리가 있는 동영상은 대사를 오디오로만 전달하므로, 청각 장애가 있거나 잘 듣지 못하는 시청자는 자막 없이는 아무것도 얻지 못합니다. WCAG 1.2.2 자막(사전 녹화)은 자막을 요구합니다. `<video>` 안에 `kind`가 `captions`나 `subtitles`인 `<track>`이 있으면 규칙을 충족하며, `kind`가 아예 없는 `<track>`도 기본값이 `subtitles`이므로 충족합니다.

`muted` 동영상은 자막을 달 오디오가 없으므로 보고하지 않습니다. 여는 태그나 본문에 템플릿 태그가 있는 동영상도 보고하지 않습니다. 트랙이나 `muted` 속성을 djLint가 볼 수 없는 곳에서 템플릿이 쓸 수 있기 때문입니다. 여기서 템플릿 태그는 템플릿 언어가 여는 `{{`, `{%`, `{#`, `${`를 뜻하므로, `onclick="$(this).play()"` 같은 jQuery 핸들러, Alpine의 `$refs`, CSS 중괄호, 대체 텍스트에 쓴 가격은 보이는 그대로 일반 텍스트이며 동영상은 여전히 검사합니다.

`muted`는 속성이어야 하므로 `<video class=muted>`는 muted라는 이름의 클래스일 뿐이고 보고합니다. 주석 처리되었거나 속성 값 안에 쓴 `<track>`은 트랙이 아니라 텍스트입니다. 값 안의 `</video>`는 아무것도 끝내지 않으며, 요소는 실제 끝 태그가 닫는 위치에서 판단하므로, 열린 채로 남은 `<video>`는 `H025`에 맡깁니다.

잘못된 예:

```html
<video controls src="talk.mp4"></video>
```

올바른 예:

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

{% endraw %}

<!-- oxfmt-ignore-end -->

### 규칙 추가하기

새 규칙을 담은 풀 리퀘스트를 환영합니다!

좋은 규칙은 다음으로 구성됩니다.

::: content

- 이름
- 코드
- 메시지: 오류를 찾았을 때 표시할 메시지입니다.
- 플래그: re.I|re.M 같은 정규식 플래그입니다. 기본값은 re.DOTALL입니다.
- 패턴: 오류를 찾아내는 정규식입니다.
- 제외: 규칙을 적용하지 않을 프로필의 목록입니다(선택 사항).
:::

규칙을 검증하는 테스트도 함께 포함해 주세요.

## 사용자 정의 규칙

`pyproject.toml` 옆에 `.djlint_rules.yaml`을 만들면 프로젝트 전용 사용자 정의 규칙을 추가할 수 있습니다. 이 파일에 규칙을 추가하면 djLint가 읽어 들입니다. 다른 위치에 있는 규칙 파일은 `--rules` CLI 옵션으로 지정할 수 있습니다.

### 패턴 규칙

정규식 패턴 중 하나라도 일치하면 실패하는 규칙을 추가할 수 있습니다.

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Python 모듈 규칙

사용자 정의 Python 함수를 임포트해 실행하는 규칙을 추가할 수 있습니다.

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

지정한 `python_module`에는 검사하는 모든 파일마다 실행될 `run()` 함수가 있어야 합니다. 이 함수는 다음 인수를 받아야 합니다.

::: content

- `rule`: `.djlint_rules.yaml`에 있는 규칙을 나타내는 dict입니다. 보통 이 변수로 규칙 이름과 메시지에 접근합니다.
- `config`: DJLint 구성 객체입니다.
- `html`: 파일의 전체 HTML 내용입니다.
- `filepath`: 현재 검사 중인 파일의 경로입니다.
- `line_ends`: 각 줄의 `start`와 `end` 문자 위치 목록입니다. `djlint.lint.get_line()`과 함께 사용하면 문자 위치에서 줄 번호를 얻을 수 있습니다. 예시를 참고하세요.
- `*args, **kwargs`: 앞으로 다른 인수가 추가될 수 있으므로, djLint를 업그레이드할 때 실패할 위험을 줄이려면 이 두 인수를 포함해야 합니다.
:::

모듈은 프로젝트 루트에 둘 수 있습니다. 함수가 위치가 아닌 `line`이나 `end`를 반환하면 djLint는 규칙 이름을 밝히는 오류와 함께 멈춥니다.

함수는 오류마다 하나씩, 다음 키를 가진 dict의 리스트를 반환해야 합니다.

::: content

- `code`: 오류를 보고하는 규칙의 코드 이름입니다(보통 `rule['name']`).
- `line`: 줄 번호와 그 줄에서의 문자 번호를 ':'로 구분한 문자열입니다.
  예를 들어 `"2:3"`은 2번째 줄의 3번째 문자에서 오류를 찾았다는 뜻입니다.
- `end`: 선택 사항입니다. 오류가 끝나는 위치로, `line`과 같은 형식으로 마지막 문자의 바로 다음 위치를 씁니다. 지정하지 않으면 오류는 `match`가 끝나는 곳에서 끝납니다.
- `match`: 내용 중 오류가 있는 부분입니다.
- `message`: 오류를 알리기 위해 출력할 메시지입니다(보통 `rule['message']`).
:::

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
