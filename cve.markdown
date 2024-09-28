---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: CVEs 
permalink: /cve/
---

{% for cve in site.data.cve %}

# [{{ cve.title }}]({{cve.url}})

{% endfor %}

