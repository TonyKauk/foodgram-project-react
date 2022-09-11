from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from .views import (
    TagViewSet, UserViewSet, IngredientViewSet, RecipeViewSet,
    IngredientAmountViewSet, CartViewSet
)


router = DefaultRouter()

router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredientamount', IngredientAmountViewSet)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
#    'recipes/65/shopping_cart/',
    CartViewSet,
    basename='carts'
    )

# router_auth.register(
#     'token', TokenViewSet, basename='tokens'
# )
# router_auth.register(
#     'signup', SingupViewSet, basename='signups'
# )
# 
# router.register(
#     'users', UserViewSet, basename='users'
# )
# router.register(
#     r'categories', CategoryViewSet, basename='categories'
# )
# router.register(
#     r'genres', GenreViewSet, basename='genres'
# )
# router.register(
#     r'titles', TitleViewSet, basename='titles'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews',
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments',
# )
# 
# 

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
#    path('recipes/<int:id>/shopping_cart/', CartView.as_view()),
#    path(r'recipes/(?P<id>\d+)/shopping_cart/', CartView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
]
