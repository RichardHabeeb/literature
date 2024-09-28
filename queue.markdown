---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: Read Queue
permalink: /queue/
---

{% for category in site.data.queue %}

## {{ category.name }}

{% assign queue = category.queue | newline_to_br | strip_newlines | split: '<br />' %}
{% for paper in queue %}
- {{ paper | remove: lcurly | remove: rcurly  }}
{% endfor %}

---

{% endfor %}
