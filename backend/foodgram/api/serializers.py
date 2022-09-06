# import datetime as dt
import base64

from django.core.files.base import ContentFile
from requests import request
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from recipes.models import (
    Tag, Ingredient, Recipe, IngredientAmount, FavoriteRecipe, Cart,
    )
# from rest_framework.validators import UniqueValidator

from users.models import User
from recipes.models import FollowAuthor


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ListRetrieveUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, user):
        if self.context['request'].auth is None:
            return False
        current_user = self.context['request'].user
        return FollowAuthor.objects.filter(
            user=current_user,
            author=user,
        ).exists()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'id',
        ]


class UserPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=200)
    current_password = serializers.CharField(max_length=200)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug',
        ]


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]


class IngredientAmountListRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    def get_id(self, ingredientamount):
        ingredient_id = ingredientamount.name.id
        return ingredient_id

    def get_measurement_unit(self, ingredientamount):
        ingredient_unit = ingredientamount.name.measurement_unit
        return ingredient_unit

    class Meta:
        model = IngredientAmount
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class IngredientAmountCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        source='name',
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = IngredientAmount
        fields = [
            'id',
            'amount',
        ]


class RecipeListRetrieveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = ListRetrieveUserSerializer(read_only=True, many=False)
    ingredients = IngredientAmountListRetrieveSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    def get_is_favorited(self, recipe):
        if self.context['request'].auth is None:
            return False
        user = self.context['request'].user
        return FavoriteRecipe.objects.filter(
            user=user,
            recipe=recipe,
        ).exists()

    def get_is_in_shopping_cart(self, recipe):
        if self.context['request'].auth is None:
            return False
        user = self.context['request'].user
        return Cart.objects.filter(
            user=user,
            recipe=recipe,
        ).exists()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]


class RecipePostUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientAmountCreateUpdateSerializer(
        read_only=False,
        many=True,
    )
    image = Base64ImageField(required=True, allow_null=True)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        author = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data, author=author)

        for tag in tags:
            recipe.tags.add(tag)

        for ingredient in ingredients:
            ingredient_amount = IngredientAmount.objects.create(
                name=ingredient['name'],
                amount=ingredient['amount'],
            )
            ingredient_amount_id = ingredient_amount.id
            recipe.ingredients.add(ingredient_amount_id)
        return recipe

    def update(self, validated_data):
        return validated_data

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        ]


# ########################################################################
# class UserListRetrieveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
# #            'is_subscribed',
#         ]
# 
# 
# class SignupSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         validators=(UniqueValidator(queryset=User.objects.all()),)
#     )
#     username = serializers.CharField(
#         validators=(UniqueValidator(queryset=User.objects.all()),)
#     )
#     first_name = serializers.CharField(max_length=150)
#     last_name = serializers.CharField(max_length=150)
# 
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#         )
# 
# 
# class UserPasswordResetSerializer(serializers.Serializer):
#     new_password = serializers.CharField(max_length=200)
#     current_password = serializers.CharField(max_length=200)
# 
# 
# class TokenSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=200)
#     email = serializers.EmailField(max_length=100)
# ########################################################################

# class TokenSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     confirmation_code = serializers.CharField(max_length=100)
# 
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'confirmation_code',
#         )


# class SignupSerializer(serializers.Serializer):
#     username = serializers.CharField(
#         validators=(UniqueValidator(queryset=User.objects.all()),)
#     )
#     email = serializers.EmailField(
#         validators=(UniqueValidator(queryset=User.objects.all()),)
#     )
# 
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#         )
# 
#     def validate_username(self, value):
#         if value == 'me':
#             raise serializers.ValidationError(
#                 'Никнейм "me" запрещен.'
#             )
#         return value
# 
# 
# class TokenSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     confirmation_code = serializers.CharField(max_length=100)
# 
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'confirmation_code',
#         )
# 
# 
# class CategorySerializer(serializers.ModelSerializer):
# 
#     class Meta:
#         fields = (
#             'name',
#             'slug'
#         )
#         lookup_field = 'slug'
#         model = Category
# 
# 
# class GenreSerializer(serializers.ModelSerializer):
# 
#     class Meta:
#         fields = (
#             'name',
#             'slug',
#         )
#         lookup_field = 'slug'
#         model = Genre
# 
# 
# def validate_year(value):
#     if value > dt.datetime.now().year:
#         raise serializers.ValidationError(
#             'Год выпуска не может быть больше текущего'
#         )
#     return value
# 
# 
# class TitleGetSerializer(serializers.ModelSerializer):
#     description = serializers.CharField(required=False)
#     year = serializers.IntegerField(validators=[validate_year])
#     genre = GenreSerializer(many=True, read_only=True)
#     category = CategorySerializer()
#     rating = serializers.IntegerField(
#         source='reviews__score__avg',
#         read_only=True
#     )
# 
#     class Meta:
#         fields = (
#             'id',
#             'name',
#             'year',
#             'rating',
#             'description',
#             'genre',
#             'category',
#         )
#         model = Title
# 
# 
# class TitleSerializer(serializers.ModelSerializer):
#     description = serializers.CharField(required=False)
#     year = serializers.IntegerField(validators=[validate_year])
#     genre = serializers.SlugRelatedField(
#         many=True,
#         slug_field='slug',
#         queryset=Genre.objects.all()
#     )
#     category = serializers.SlugRelatedField(
#         slug_field='slug',
#         queryset=Category.objects.all()
#     )
# 
#     class Meta:
#         fields = (
#             'id',
#             'name',
#             'year',
#             'description',
#             'genre',
#             'category',
#         )
#         model = Title
# 
# 
# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#         default=serializers.CurrentUserDefault()
#     )
# 
#     class Meta:
#         model = Comment
#         fields = ('id', 'text', 'author', 'pub_date')
# 
# 
# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         many=False,
#         read_only=True,
#         slug_field='username',
#         default=serializers.CurrentUserDefault(),
#     )
# 
#     class Meta:
#         model = Review
#         fields = ('id', 'text', 'author', 'score', 'pub_date')
#         read_only_fields = ('id', 'author', 'pub_date')
# 
#     def validate_score(self, value):
#         if value < 1 or value > 10:
#             raise serializers.ValidationError(
#                 'Пожалуйста, только целые числа от 1 до 10'
#             )
#         return value
# 
#     def validate(self, data):
#         title_id = self.context['view'].kwargs.get('title_id')
#         author = self.context.get('request').user
#         title = get_object_or_404(Title, id=title_id)
#         if title.reviews.filter(author=author).exists() and (
#             self.context.get('request').method == 'POST'
#         ):
#             raise serializers.ValidationError(
#                 'Вы уже оставляли здесь отзыв. До новых встреч.'
#             )
#         return data
# 