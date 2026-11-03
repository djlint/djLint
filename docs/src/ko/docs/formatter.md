---
description: djLint가 HTML 템플릿을 포맷하는 방식과, 변경 사항을 적용하기 전에 확인하는 방법입니다.
title: 포맷터 사용법
keywords: 템플릿 린터, 템플릿 포맷터, djLint, HTML, 템플릿, 포맷터, 린터, 포맷터 사용법
---

# 포맷터 사용법

djLint의 포맷터는 엉성한 HTML 템플릿을 받아 일관되고 읽기 쉬운 형태로 포맷합니다!

변경 사항을 적용하기 전에 `--check`로 결과를 검토하세요.

포맷하면 무엇이 바뀌는지 검토하려면 다음을 실행합니다.

```bash
djlint . --check --single-attribute-per-line
```

코드를 포맷하고 파일을 업데이트하려면 다음을 실행합니다.

```bash
djlint . --reformat --single-attribute-per-line

# 스크립트와 스타일도 포맷하려면?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">모든 옵션은 구성 가이드에서 확인하세요!</a></div>
</div>

{% admonition
   "note",
   "참고",
   "속성 안에 작성한 JSON과 JavaScript는 `--format-attribute-js-json`을 켜지 않으면 그대로 둡니다. 속성 안의 HTML은 항상 그대로 둡니다."
%}

{% admonition
   "note",
   "참고",
   "djLint는 HTML 파서나 구문 검사기가 아닙니다."
%}

## 예시를 살펴봅시다!

### 포맷 전

손질이 절실하게 필요한 HTML 덩어리입니다.

{% raw %}

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
{% if pagination_required %}
{% for i in page_range %}
{% paginator_number cl i %}
{% endfor %}
{% endif %}
{{ cl.result_count }}
{% if cl.result_count == 1 %}
{{ cl.opts.verbose_name }}
{% else %}
{{ cl.opts.verbose_name_plural }}
{% endif %}
{% if show_all_url %}
<a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}</a>
{% endif %}
{% if cl.formset and cl.result_count %}
<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">
{% endif %}
</p>
```

{% endraw %}

### 포맷 후

이제 조금 나아 보입니다... 읽을 수는 있겠네요 :)

{% raw %}

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}
    {{ cl.result_count }}
    {% if cl.result_count == 1 %}
        {{ cl.opts.verbose_name }}
    {% else %}
        {{ cl.opts.verbose_name_plural }}
    {% endif %}
    {% if show_all_url %}
        <a href="{{ show_all_url }}" class="showall">{% translate "Show all" %}</a>
    {% endif %}
    {% if cl.formset and cl.result_count %}
        <input type="submit"
               name="_save"
               class="default"
               value="{% translate 'Save' %}">
    {% endif %}
</p>
```

{% endraw %}

### `single_attribute_per_line` 옵션으로 포맷한 후

Prettier 스타일의 속성 배치를 선호하나요? `single_attribute_per_line` 옵션을 켜세요.

{% raw %}

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}
    {{ cl.result_count }}
    {% if cl.result_count == 1 %}
        {{ cl.opts.verbose_name }}
    {% else %}
        {{ cl.opts.verbose_name_plural }}
    {% endif %}
    {% if show_all_url %}
        <a href="{{ show_all_url }}" class="showall">{% translate "Show all" %}</a>
    {% endif %}
    {% if cl.formset and cl.result_count %}
        <input
            type="submit"
            name="_save"
            class="default"
            value="{% translate 'Save' %}"
        >
    {% endif %}
</p>
```

{% endraw %}
