from django.db.models import Sum

from recipes.models import IngredientAmount


def create_list_of_ingredients(user_id):
    ingredients = IngredientAmount.objects.filter(
        recipes__recipe_added_to_cart__user=user_id).values(
            'name__name',
            'name__measurement_unit'
        ).annotate(Sum('amount'))
    list_of_ingredients = 'Список ингредиентов: \n\n'
    for ingredient in ingredients:
        name = ingredient['name__name']
        unit = ingredient['name__measurement_unit']
        amount = ingredient['amount__sum']
        list_of_ingredients += f'{name} ({unit}) - {amount}\n'
    return list_of_ingredients
