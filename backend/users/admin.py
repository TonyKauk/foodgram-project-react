from django.contrib import admin

from recipes.admin import Admin
from .models import FollowAuthor, User


admin.site.register(User, Admin)
admin.site.register(FollowAuthor, Admin)
