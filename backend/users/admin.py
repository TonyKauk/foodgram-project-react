from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from recipes.admin import Admin
from .models import FollowAuthor, User


class AdminForUser(UserAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(User, AdminForUser)
admin.site.register(FollowAuthor, Admin)
