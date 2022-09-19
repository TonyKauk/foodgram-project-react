from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Recipe, Tag, Ingredient, IngredientAmount
from .models import FollowAuthor, FavoriteRecipe, Cart
# from users.models import User


class Admin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


admin.site.register(Recipe, Admin)
admin.site.register(Tag, Admin)
admin.site.register(Ingredient, Admin)
# admin.site.register(IngredientAmount, Admin)
# admin.site.register(FollowAuthor, Admin)
# admin.site.register(FavoriteRecipe, Admin)
# admin.site.register(Cart, Admin)


admin.site.unregister(User)


# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     pass


admin.site.register(User, Admin)
