from rest_framework import permissions


class AuthorOrGetOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        search_for_tags = (
            'author' and 'is_favorited' and 'is_in_shopping_cart'
        ) not in request.query_params
        return request.method == 'GET' and search_for_tags

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'DELETE'):
            return obj.author == request.user
        return True
