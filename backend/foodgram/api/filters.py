from django_filters import rest_framework

from recipes.models import (
    Tag, Ingredient, Recipe, IngredientAmount, Cart,
    FavoriteRecipe, FollowAuthor
)


class RecipeFilter(rest_framework.FilterSet):

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
        # fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
