---
title: "모범 사례"
description: "djLint로 HTML 템플릿을 포맷할 때의 모범 사례입니다."
sidebar:
  label: "모범 사례"
---

## 조건부 속성 주변의 공백

태그에 클래스를 추가할 때 조건문을 사용하기도 합니다. djLint는 조건문 내부의 공백을 제거합니다.

다음 패턴을 권장합니다.

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

다음 패턴은 권장하지 않습니다.

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags`와 공백 없는 조건부 속성

`format_attribute_template_tags` 옵션을 켰다면 조건부 속성에는 태그 내부의 공백을 제거하는 공백 제거 태그를 사용해야 합니다. 예를 들어 nunjucks와 jinja에서는 `{% if a -%}`처럼 씁니다.

djLint는 긴 속성을 여러 줄로 나누어 포맷하므로, 속성 안에 남은 공백 때문에 코드가 깨질 수 있습니다.

다음 패턴을 권장합니다.

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

표시된 위치는 모두 공백 제거 태그입니다.

다음 패턴은 권장하지 않습니다.

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

포맷하고 나면 다음과 같이 될 수 있습니다.

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
