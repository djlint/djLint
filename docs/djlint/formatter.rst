Formatter
=========

djLint's formatter will take sloppy html templates and make it look pretty nice!

For an example of what the output will be, check out the `/tests/ <https://github.com/Riverside-Healthcare/djlint/tree/master/tests>`_ folder to see over 300 **formatted** templates from the top django and flask projects.

Before
------
.. code :: html

   {% load admin_list %}   {% load i18n %}
   <p class="paginator">
       {% if pagination_required %}
   {% for i in page_range %}          {% paginator_number cl i %}
          {% endfor %}       {% endif %}
       {{ cl.result_count }}
       {% if cl.result_count == 1 %}{{ cl.opts.verbose_name }}   {% else %}
   {{ cl.opts.verbose_name_plural }}       {% endif %}
   {% if show_all_url %} <a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}
          </a>
  {% endif %}{% if cl.formset and cl.result_count %}<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">{% endif %}
                     </p>

After
-----
.. code :: html

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
           <a href="{{ show_all_url }}" class="showall">
               {% translate 'Show all' %}
           </a>
       {% endif %}
       {% if cl.formset and cl.result_count %}
           <input type="submit" name="_save" class="default" value="{% translate 'Save' %}">
       {% endif %}
   </p>
