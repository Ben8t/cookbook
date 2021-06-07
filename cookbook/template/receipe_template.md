# {{name}}

![]({{img}})

[Voir la recette sur Le Journal Des Femmes - Cuisine]({{url}})

!!! info
{% for resume in recipe_resume %}
    **{{resume.strong}}**: {{resume.flat}}
{%- endfor %}



!!! example "Ingrédients"
{% for ingredient in recipe_ingredients %}
    ![]({{ingredient.img}}) {{ingredient.name}} - {{ingredient.quantity}}
{% endfor -%}

---

{% for preparation in recipe_preparations %}
**{{preparation.etape}}**. {{preparation.text}}
{% endfor -%}