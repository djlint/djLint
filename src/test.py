import regex as re

string = """<span title="{% if eev.status == eev.STATUS_CURRENT %} {% trans 'A' %} {% elif eev.status == eev.STATUS_APPROVED %} {% trans 'B' %} {% elif eev.status == eev.STATUS_EXPIRED %} {% trans 'C' %}{% endif %}" class="asdf {%if a%}b{%endif%} asdf" {%if a%}checked{%endif%}>"""

regex = r"""(?<!\n[ ]*?)\K(<span[ ]+?(
             (?:[^\s]+?=(?:\'(?:[^\']*?{%[^}]*?%}[^\']*?)+?\'))
        )\s*?>)"""

print(re.findall(regex, string, re.I | re.X))
