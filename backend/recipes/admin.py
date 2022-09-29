from django.contrib import admin

from .models import (
    Cart, FavoriteRecipe, Ingredient, IngredientAmount, Recipe, Tag,
)


class Admin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class RecipeAdmin(Admin):
    list_display = ('name', 'author', 'times_favorited')
    list_filter = ('name', 'author', 'tags')

    def times_favorited(self, object):
        return object.added_to_favorite.count()


class IngredientAdmin(Admin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, Admin)
admin.site.register(IngredientAmount, Admin)
admin.site.register(FavoriteRecipe, Admin)
admin.site.register(Cart, Admin)
