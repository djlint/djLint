---
title: "포맷터 사용법"
description: "djLint가 HTML 템플릿을 포맷하는 방식과, 변경 사항을 적용하기 전에 확인하는 방법입니다."
sidebar:
  label: "포맷터"
---

djLint의 포맷터는 HTML 템플릿의 레이아웃을 일관되게 맞춥니다. 먼저 무엇이 바뀌는지 확인하세요.

```bash
djlint . --check --format-css --format-js
```

그런 다음 파일을 그 자리에서 포맷합니다. 이 예시에서는 `<style>`과 `<script>`의 내용도 포맷합니다.

```bash
djlint . --reformat --format-css --format-js
```

:::note[참고]
속성 안에 작성한 JSON과 JavaScript는 `--format-attribute-js-json`을 켜지 않으면 그대로 둡니다. 속성 안의 HTML은 항상 그대로 둡니다.
:::

:::note[참고]
djLint는 HTML 파서나 구문 검사기가 아닙니다.
:::

## 예시

### 포맷 전

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

### 포맷 후

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

### `single_attribute_per_line` 옵션으로 포맷한 후

Prettier 스타일의 속성 배치를 선호하나요? `single_attribute_per_line` 옵션을 켜세요.

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
