<div class="tabs">
<ul>
<li class="is-active"><a tab="pyproject-toml-tab">pyproject.toml</a></li>
<li><a tab="djlint-toml-tab">djlint.toml / .djlint.toml</a></li>
<li><a tab="djlintrc-tab">.djlintrc</a></li>
</ul>
</div>

<div class="tab-container">
<div class="tab is-active" id="pyproject-toml-tab">

```toml
[tool.djlint]
profile="{{ tool }}"
```

</div>
<div class="tab" id="djlint-toml-tab">

```toml
profile="{{ tool }}"
```

</div>
<div class="tab" id="djlintrc-tab">

```json
{ "profile": "{{ tool }}" }
```

</div>
</div>

{% include 'src/_includes/tabs_script.njk' %}
