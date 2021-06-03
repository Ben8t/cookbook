# {{name}}

![]({{img}})

[]({{url}})

!!! info
{% for resume in recipe_resume %}
    **{{resume.strong}}**: {{resume.flat}}
{%- endfor -%}