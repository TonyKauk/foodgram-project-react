from django.contrib import admin

from .models import Recipe, Tag, Ingredient, IngredientAmount
from .models import FollowAuthor, FavoriteRecipe, Cart


admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(FollowAuthor)
admin.site.register(FavoriteRecipe)
admin.site.register(Cart)
