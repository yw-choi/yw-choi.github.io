---
layout: default
title: Staff
---
# Staff

{% for author in site.authors %}
- ## <a href="{{ author.url }}">{{ author.name }}</a>
  ### {{ author.position }}
  {{ author.content | markdownify }}
{% endfor %}
