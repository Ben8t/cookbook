# {{name}}

![]({{img}})

[Voir la recette sur Le Journal Des Femmes - Cuisine]({{url}})

!!! info
{% for resume in recipe_resume %}
    **{{resume.strong}}**: {{resume.flat}}
{%- endfor %}


=== "Pour 2"
    !!! example "Ingrédients"
    {% for ingredient in recipe_ingredients %}
        ![]({{ingredient.img}}) {{ingredient.name}} - {{ingredient.quantity2}} {{ingredient.quantity_title}}
    {% endfor %}

=== "Pour 4"
    !!! example "Ingrédients"
    {% for ingredient in recipe_ingredients %}
        ![]({{ingredient.img}}) {{ingredient.name}} - {{ingredient.quantity4}} {{ingredient.quantity_title}}
    {% endfor %}

=== "Pour 6"
    !!! example "Ingrédients"
    {% for ingredient in recipe_ingredients %}
        ![]({{ingredient.img}}) {{ingredient.name}} - {{ingredient.quantity6}} {{ingredient.quantity_title}}
    {% endfor %}

---

## Préparation

{% for preparation in recipe_preparations %}
**{{preparation.etape}}**. {{preparation.text}}
{% endfor -%}