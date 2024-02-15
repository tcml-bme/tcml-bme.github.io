---
layout: page
title: Papers tagged "Cardiac"
---

{% assign articles = site.articles | where: 'categories', 'Cardiac' %}

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
