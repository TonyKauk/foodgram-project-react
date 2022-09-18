from rest_framework import permissions


# class NotAuthenticatedUsersListRetrieve(permissions.BasePermission):
#     def has_permission(self, request, view):
#         search_for_tags = (
#             'author' and 'is_favorited' and 'is_in_shopping_cart'
#         ) not in request.query_params
#         return (
#             (request.method in permissions.SAFE_METHODS) and search_for_tags
#         )


# class NotAuthenticatedUsersPost(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.method == 'POST'


class RecipeAuthorPatchDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        auth = request.user.is_authenticated
        return (request.method is ('PATCH' or 'DELETE') and auth)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


#############################################################################
# class IsAdminOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_admin)
# 
#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_admin)
# 
# 
# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_admin
# 
# 
# class IsAdminModerAuthorAuthenticatedOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated)
# 
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if request.method == 'POST':
#             return request.user.is_authenticated
#         if request.user.is_authenticated:
#             allowed = (
#                 obj.author == request.user,
#                 request.user.is_admin,
#                 request.user.is_moderator,
#             )
#             return any(allowed)
#         return False
# 