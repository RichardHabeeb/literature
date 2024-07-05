---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

{% capture lcurly -%}{% raw %}}{% endraw %}{%- endcapture %}
{% capture rcurly -%}{% raw %}{{% endraw %}{%- endcapture %}

{% for paper in site.data.papers %}

{% capture venue -%}
{%- if paper.journal -%}
{{- paper.journal -}}
{%- else -%}
{{- paper.booktitle | default: "Unknown Venue" -}}
{%- endif -%}
{%- endcapture %}

{% capture title -%}
	{%- if paper.year -%}
		( {{- paper.year -}}
		{%- if site.data.venues[venue] -%}
			{{- site.data.venues[ venue ] | prepend: ' ' -}}
		{%- endif -%}
		)
	{%- endif -%}
	{{- paper.title | prepend: ' ' -}}
{%- endcapture %}
{% assign title = title | remove: lcurly | remove: rcurly %}


{% if paper.doi %}
# [{{ title }}](https://doi.org/{{paper.doi}})
{% elsif paper.url %}
# [{{ title }}]({{paper.url}})
{% else %}
# {{ title }}
{% endif %}

{% if paper.author %}
{% assign rawAuthors = paper.author | split: ' and ' %}

{% capture authors -%}
{%- for author in rawAuthors -%}
[{{- author | split: ',' | reverse | join: ' ' -}}](https://scholar.google.com/citations?view_op=search_authors&mauthors=
{{- author | split: ',' | reverse | join: '+' -}}
&hl=en&oi=ao);
{%- endfor -%}
{%- endcapture -%}


*{{ authors | split: ';' | join: ',' | remove: lcurly | remove: rcurly }}*
{% endif %}

### **{{ venue | remove: lcurly | remove: rcurly }}**

---

{% endfor %}
