from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet, UserViewSet, IngredientViewSet, RecipeViewSet,
    IngredientAmountViewSet, CartViewSet, FavoriteViewSet,
    FollowAuthorViewSet,
)


router = DefaultRouter()

router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredientamount', IngredientAmountViewSet)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    CartViewSet,
    basename='carts'
    )
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorites'
    )
router.register(
    r'users/(?P<user_id>\d+)/subscribe',
    FollowAuthorViewSet,
    basename='carts'
    )

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
