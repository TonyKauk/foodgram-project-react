from django_filters import rest_framework

from recipes.models import Recipe, Tag
from users.models import User


class ResipesFilter(rest_framework.FilterSet):
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    author = rest_framework.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = rest_framework.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = rest_framework.NumberFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def get_is_favorited(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(
                added_to_favorite__user=self.request.user
            )
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(
                recipe_added_to_cart__user=self.request.user
            )
        return Recipe.objects.all()
