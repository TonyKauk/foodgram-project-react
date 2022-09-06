# from django.conf import settings
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.core.mail import send_mail
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
# from rest_framework.exceptions import MethodNotAllowed
# from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view
# 
# from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet, ListRetrieveCreateViewSet
from recipes.models import (
    Tag, Ingredient, Recipe, IngredientAmount, Cart
)
# from .permissions import (
#     IsAdmin, IsAdminOrReadOnly, IsAdminModerAuthorAuthenticatedOrReadOnly
# )
from .serializers import (
    ListRetrieveUserSerializer, TagSerializer, IngredientSerializer,
    RecipeListRetrieveSerializer, UserSignUpSerializer,
    UserPasswordResetSerializer, IngredientAmountListRetrieveSerializer,
    RecipePostUpdateSerializer,
    )

from users.models import User


class UserViewSet(ListRetrieveCreateViewSet):
    queryset = User.objects.all()
    serializer_class = ListRetrieveUserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSignUpSerializer
        return ListRetrieveUserSerializer

    @action(methods=('GET',), url_path='me', detail=False)
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)

        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=('POST',), url_path='set-password', detail=False)
    def set_password(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.password = serializer.data['new_password']
        user.save()
        return Response(status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientAmountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountListRetrieveSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action == ('list' or 'retrieve'):
            return RecipeListRetrieveSerializer
        return RecipePostUpdateSerializer


class CartView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        recipe_id = request.kwargs.get('id')
        recipe = Recipe.objects.get(id=recipe_id)
        user = request.user
        Cart.objects.add(user=user, recipe=recipe)
        return Response(
            {
                'id': f'{recipe.id}',
                'name': f'{recipe.name}',
                'image': f'{recipe.image}',
                'cooking_time': f'{recipe.cooking_time}'
            }, status=status.HTTP_200_OK
        )

    def delete(self, request):
        pass

    return


#    def get_serializer_class(self):
#        if self.action == 'list' or 'retrieve':
#            return RecipeListRetrieveSerializer
#        return RecipePostUpdateSerializer

#    def perform_create(self, serializer):
#        author = self.request.user
#        serializer.save(author=author)



# class UserPasswordResetViewSet(viewsets.ModelViewSet):
#     serializer_class = UserPasswordResetSerializer
# 
#     def get_queryset(self, request):
#         user = get_object_or_404(User, username=request.user.username)
#         return user
# 
#     def create(self, request):
#         user = self.get_queryset()
#         serializer = UserPasswordResetSerializer(data=request.data)
#         user.password = serializer.new_password
#         user.save()
#         return Response(status=status.HTTP_200_OK)


# ########################################################################
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserListRetrieveSerializer
# 
#     @action(
#         detail=False, methods=('GET',),
#         url_path='me',  # permission_classes=(IsAuthenticated,)
#     )
#     def me(self, request):
#         user = get_object_or_404(User, username=request.user.username)
# 
#         serializer = UserListRetrieveSerializer(
#             user,
#             context={'request': request},
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save(role=user.role)
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )
# ########################################################################

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated, IsAdmin)
#     serializer_class = UserSerializer
#     filter_backends = (DjangoFilterBackend,)
#     search_fields = ('username',)
#     lookup_field = 'username'
# 
#     @action(
#         detail=False, methods=('GET', 'PATCH'),
#         url_path='me', permission_classes=(IsAuthenticated,)
#     )
#     def me(self, request):
#         user = get_object_or_404(User, username=request.user.username)
# 
#         if request.method != 'PATCH':
#             serializer = self.get_serializer(user)
#             return Response(serializer.data)
#         serializer = UserSerializer(
#             user,
#             context={'request': request},
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save(role=user.role)
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )


# class SingupViewSet(viewsets.ModelViewSet):
#     querryset = User.objects.all()
#     permission_classes = (AllowAny,)
# 
#     def create(self, request):
#         serializer = SignupSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data.get('username')
#         email = serializer.validated_data.get('email').lower()
#         user, created = User.objects.get_or_create(
#             email=email,
#             username=username
#         )
#         confirmation_code = (
#             PasswordResetTokenGenerator().make_token(user)
#         )
#         message = f'Код подтверждения - {confirmation_code}'
#         send_mail(
#             'Ваш код подтверждения',
#             message,
#             settings.EMAIL_FROM,
#             (email, )
#         )
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )
# 
# 
# class TokenViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
# 
#     def create(self, request):
#         code_test = PasswordResetTokenGenerator()
#         serializer = TokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = get_object_or_404(
#             User,
#             username=serializer.validated_data.get('username')
#         )
#         confirmation_code = serializer.validated_data.get('confirmation_code')
#         if not code_test.check_token(user, confirmation_code):
#             return Response(
#                 {'confirmation_code': ['Код не действителен!']},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         user.is_active = True
#         user.save()
#         token = AccessToken.for_user(user)
#         return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
# 
# 
# class CategoryViewSet(ListCreateDestroyViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly,
#         IsAdminOrReadOnly
#     ]
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)
#     lookup_field = 'slug'
# 
# 
# class GenreViewSet(ListCreateDestroyViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly,
#         IsAdminOrReadOnly
#     ]
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)
#     lookup_field = 'slug'
# 
# 
# class TitleViewSet(viewsets.ModelViewSet):
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly,
#         IsAdminOrReadOnly
#     ]
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = TitleFilter
#     queryset = Title.objects.all().annotate(
#         Avg('reviews__score')
#     )
# 
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return TitleGetSerializer
#         else:
#             return TitleSerializer
# 
# 
# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = (IsAdminModerAuthorAuthenticatedOrReadOnly,)
# 
#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id, title=title)
#         return review.comments.all()
# 
#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id, title=title)
#         serializer.save(author=self.request.user, review_id=review.id)
# 
# 
# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     permission_classes = (IsAdminModerAuthorAuthenticatedOrReadOnly,)
# 
#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         return title.reviews.all()
# 
#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         serializer.save(author=self.request.user, title_id=title.id)
# 
#     def update(self, request, *args, **kwargs):
#         if request.method == 'PUT':
#             raise MethodNotAllowed(method='PUT')
#         return super().update(request, *args, **kwargs)