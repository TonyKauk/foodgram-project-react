from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    Cart, FavoriteRecipe, Ingredient, Recipe, Tag
)
from users.models import FollowAuthor, User
from .functions import create_list_of_ingredients
from .mixins import CreateDestroyViewSet, ListRetrieveCreateViewSet
from .pagination import CustomPagination
from .permissions import AuthorOrGetOrReadOnly
from .serializers import (
    FollowAuthorSerializer, IngredientSerializer, ListRetrieveUserSerializer,
    RecipeListRetrieveSerializer, RecipePostToCartSerializer,
    RecipePostUpdateSerializer, TagSerializer, UserPasswordResetSerializer,
    UserSignUpSerializer,
)


class UserViewSet(ListRetrieveCreateViewSet):
    queryset = User.objects.all()
    serializer_class = ListRetrieveUserSerializer
    pagination_class = CustomPagination
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSignUpSerializer
        return ListRetrieveUserSerializer

    @action(
        methods=('GET',),
        url_path='me',
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        current_user = get_object_or_404(User, username=request.user.username)
        serializer = self.get_serializer(current_user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=('POST',),
        url_path='set_password',
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def set_password(self, request):
        current_user = get_object_or_404(User, username=request.user.username)
        serializer = UserPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user.password = serializer.data['new_password']
        current_user.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=('GET',),
        url_path='subscriptions',
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = get_object_or_404(User, username=request.user.username)
        subscriptions = User.objects.filter(
            following__user=user.id
        )

        page = self.paginate_queryset(subscriptions)

        if page is not None:
            serializer = FollowAuthorSerializer(
                page,
                context={'request': request},
                many=True
            )
            return self.get_paginated_response(serializer.data)

        serializer = FollowAuthorSerializer(
            subscriptions,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)
    permission_classes = (AuthorOrGetOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListRetrieveSerializer
        return RecipePostUpdateSerializer

    def get_queryset(self):
        current_user = self.request.user
        queryset = self.queryset
        is_favorited_filter = self.request.query_params.get('is_favorited')
        is_in_shopping_cart_filter = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        tags_filter = self.request.query_params.getlist('tags')

        if is_favorited_filter:
            if is_favorited_filter == '1':
                queryset = queryset.filter(
                    added_to_favorite__user=current_user,
                )
            else:
                queryset = queryset.exclude(
                    added_to_favorite__user=current_user,
                )

        if is_in_shopping_cart_filter:
            if is_in_shopping_cart_filter == '1':
                queryset = queryset.filter(
                    recipe_added_to_cart__user=current_user,
                )
            else:
                queryset = queryset.exclude(
                    recipe_added_to_cart__user=current_user,
                )

        if len(tags_filter) >= 0 and is_in_shopping_cart_filter is None:
            queryset = queryset.filter(
                tags__slug__in=tags_filter
            ).distinct()

        return queryset

    @action(
       methods=('GET',),
       url_path='download_shopping_cart',
       detail=False,
       permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user_id = request.user.id
        list_of_ingredients = create_list_of_ingredients(user_id=user_id)

        filename = 'list_of_ingredients.txt'
        response = HttpResponse(
            list_of_ingredients,
            content_type='text/plain; charset=UTF-8',
        )
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(filename)
        )
        return response


class CartViewSet(CreateDestroyViewSet):
    queryset = Cart.objects.all()
    serializer_class = RecipePostToCartSerializer

    def create(self, request, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)
        Cart.objects.create(user=request.user, recipe=recipe)
        data = self.serializer_class(recipe).data
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        user = request.user
        recipe = Recipe.objects.get(id=recipe_id)
        Cart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = RecipePostToCartSerializer

    def create(self, request, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)
        user = request.user
        FavoriteRecipe.objects.create(user=user, recipe=recipe)
        data = self.serializer_class(recipe).data
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        user = request.user
        recipe = Recipe.objects.get(id=recipe_id)
        FavoriteRecipe.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowAuthorViewSet(CreateDestroyViewSet):
    queryset = FollowAuthor.objects.all()
    serializer_class = FollowAuthorSerializer

    def create(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        author = User.objects.get(id=user_id)
        user = request.user
        FollowAuthor.objects.create(user=user, author=author)
        data = self.serializer_class(
            author,
            context={'request': request},
            data=request.data,
            partial=True
        )
        data.is_valid(raise_exception=True)
        return Response(data.data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        user = request.user
        author = User.objects.get(id=user_id)
        FollowAuthor.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
