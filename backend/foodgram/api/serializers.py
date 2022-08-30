# import datetime as dt
# 
from requests import request
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from recipes.models import Tag, Ingredient
# from rest_framework.validators import UniqueValidator

from users.models import User
from recipes.models import FollowAuthor


class ListRetrieveUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, user):
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