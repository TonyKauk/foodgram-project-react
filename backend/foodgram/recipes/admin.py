from django.contrib import admin

from .models import Recipe, Tag, Ingridient, IngridientAmount
from .models import FollowAuthor, FavoriteRecipe, Cart

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingridient)
admin.site.register(IngridientAmount)
admin.site.register(FollowAuthor)
admin.site.register(FavoriteRecipe)
admin.site.register(Cart)
