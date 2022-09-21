import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from recipes.models import (
    Tag, Ingredient, Recipe, IngredientAmount, FavoriteRecipe, Cart,
    )
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

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
    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),),
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
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
        required = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]

    def validate_username(self, value):
        if value == 'DELETED_USER':
            raise serializers.ValidationError(
                'Никнейм "DELETED_USER" запрещен.'
            )
        return value


class UserPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=200, required=True)
    current_password = serializers.CharField(max_length=200, required=True)


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
    ingredients = IngredientAmountListRetrieveSerializer(
        read_only=True,
        many=True,
    )
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
        queryset=Tag.objects.all(),
        required=True,
    )
    ingredients = IngredientAmountCreateUpdateSerializer(
        read_only=False,
        many=True,
        required=True,
    )
    image = Base64ImageField(required=True, allow_null=True)
    name = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        author = self.context['request'].user
        validated_data['author'] = author
        recipe = Recipe.objects.create(**validated_data)

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

    def update(self, instance, validated_data):
        tags_list = validated_data.pop('tags')
        ingredients_list = validated_data.pop('ingredients')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        recipe = instance

        recipe.tags.set(tags_list)

        recipe.ingredients.clear()
        for ingredient in ingredients_list:
            ingredient_amount = IngredientAmount.objects.create(
                **ingredient
            )
            recipe.ingredients.add(ingredient_amount.id)
        return recipe

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'author',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=['name', 'author']
            )
        ]

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Время приготовления должно быть как минимум 1 минута'
            )
        return value


class RecipePostToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]
        read_only_fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class FollowAuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, user):
        current_user = self.context['request'].user
        author = user
        return FollowAuthor.objects.filter(
            user=author,
            author=current_user,
        ).exists()

    def get_recipes(self, user):
        recipes_limit = self.context.get('request').query_params.get(
            'recipes_limit'
        )
        recipes = Recipe.objects.filter(author=user)

        if recipes_limit is not None:
            recipes = recipes[:int(recipes_limit)]

        serializer = RecipePostToCartSerializer(
            recipes,
            read_only=True,
            many=True,
        )
        return serializer.data

    def get_recipes_count(self, user):
        author = User.objects.get(id=user.id)
        count = Recipe.objects.filter(author=author).count()
        return count

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]
