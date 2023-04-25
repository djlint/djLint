---
description: Configuration de djLint pour le linting et le formatage des modèles HTML. Profitez des nombreuses options de formatage.
title: Configuration
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, configuration
---

# {{ "configuration" | i18n }}

La configuration se fait soit à travers le fichier `pyproject.toml` de votre projet, soit à travers un fichier `.djlintrc`. Les arguments de la ligne de commande remplaceront toujours les paramètres du fichier `pyproject.toml`. Les paramètres locaux du projet prévaudront toujours sur les fichiers de configuration globaux.

Le format du fichier `pyproject.toml` est `toml`.

```ini
[tool.djlint]
<options de configuration>
```

Le format du fichier `djlintrc` est `json`.

```json
{
  "option": "valeur"
}
```

## Options

<div class="field">
  <label class="label">Options de filtrage</label>
  <div class="control">
    <input id="filter" class="input" type="text" placeholder="pour filtrer les options..." />

  </div>
</div>
<script>
const hideAll=() => {
    (document.querySelectorAll('.option') || []).forEach((x) => {
                x.classList.add('is-hidden')
        })
}
const showAll=() => {
    (document.querySelectorAll('.option') || []).forEach((x) => {
                x.classList.remove('is-hidden')
        })
}
var search_data = {{ configuration | dump | safe }};
document.querySelector('#filter').addEventListener('input', (event) => {
    document.querySelector('#no-matches').classList.add('is-hidden');
      if (event.target.value === ''){
        showAll()
      } else {
        var regex = new RegExp(event.target.value.replaceAll(' ', '.*[ _-].*'), 'gmi'),
        matches=[]
        search_data.forEach((obj) => {
        if (JSON.stringify(obj).match(regex)) {
            matches.push(obj.name)
        }
        if(matches.length > 0){
            document.querySelector('#no-matches').classList.add('is-hidden');
        (document.querySelectorAll('.option') || []).forEach((x) => {
            if (matches.includes(x.getAttribute('data-name'))){
                x.classList.remove('is-hidden')
            }
            else {
                x.classList.add('is-hidden')
            }
        })} else {
            hideAll();
            document.querySelector('#no-matches').classList.remove('is-hidden');
        }
        })
        }
    })
    </script>
<hr />

{% for option in configuration | sort(false, false, "name") %}

<div class="option has-background-white-ter p-3 my-3 is-rounded" data-name="{{option.name}}">
<div class="is-flex is-justify-content-space-between">
    <h3 class="title is-3">
        <a class="link bn" href="#{{ option.name | slugify }}">∞</a> {{ option.name }}</h3>
    <div class="tags is-inline-block">{% for tag in option.tags %}<span class="tag is-family-sans-serif is-link has-text-weight-medium">{{ tag }}</span>{% endfor %}</div></div>

<p>{{ option.description[locale or "en"] | markdown | safe }}</p>

<div class="tabs">
<ul>

{% for flag in option.usage %}

<li class="{% if loop.index == 1 %}is-active{% endif %}"><a tab="{{- flag.name | slugify -}}-tab">{{ flag.name }}</a></li>

{% endfor %}

</ul>
</div>

<div class="tab-container">
{% for flag in option.usage %}
<div class="tab {% if loop.index == 1 %}is-active{% endif %}"id="{{- flag.name | slugify -}}-tab">

```{% if flag.name == "pyproject.toml" %}toml{% else %}json{% endif %}
{{ flag.value | safe }}
```

</div>
{% endfor %}

</div></div>

{% endfor %}

<div id="no-matches" class="is-hidden mb-5">Rien n'a été trouvé. Essayez une autre recherche.</div>

<script>
document.addEventListener('click', function (e) {
  if (
    e.target.closest('.tabs li a') &&
    e.target.closest('.tabs li a').hasAttribute('tab')
  ) {
    var tabLinks = document.querySelectorAll('.tabs li.is-active');
    for (var l = 0; l < tabLinks.length; l++) {
      tabLinks[l].classList.remove('is-active');
    }

    var tabs = document.querySelectorAll('.tab.is-active');

    for (var i = 0; i < tabs.length; i++) {
      tabs[i].classList.remove('is-active');
    }

    var activeBox = document.querySelectorAll('.tab#' + e.target.getAttribute('tab'))
    for(var y= 0; y < activeBox.length; y++){
      activeBox[y].classList.add('is-active');
    }

    var activeTab = document.querySelectorAll('a[tab="' + e.target.getAttribute('tab') + '"]')
    for(var y= 0; y < activeTab.length; y++){
      activeTab[y].parentElement.classList.add('is-active');
    }
  }
});
</script>
