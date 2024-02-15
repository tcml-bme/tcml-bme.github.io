---
layout: page
title: Papers tagged "T1/T2 Mapping"
---

{% assign articles = site.articles | where: 'categories', 'T1/T2 Mapping' %}

{% assign sorted = articles | reverse %}

{% for article in sorted %}
  <div class="journal-item my-4">

    {% for author in article.authors %}
      {{ author }}, 
    {% endfor %}

    <a href="https://doi.org/{{ article.DOI }}">
      <b>{{ article.title }}</b>
    </a>

    <i>
      {{ article.journal }},
    </i>

    {{ article.misc }}.

    {{ article.date | date: "%B %Y" }}

  </div>

{% endfor %}
