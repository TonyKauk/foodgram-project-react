from colorfield.fields import ColorField
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import (
    RegexValidator,  #  MinValueValidator, MaxValueValidator
)

from .functions import get_or_create_deleted_user

User = get_user_model()
deleted_user_id = get_or_create_deleted_user

MINIMUM_COOKING_TIME = 1


def validate_cooking_time(value):
    if value < MINIMUM_COOKING_TIME:
        raise ValidationError(
            'Время приготовления должно быть не меньше 1 минуты'
        )
    return value


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=deleted_user_id,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фото рецепта',
    )
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        'IngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Тэги'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления, мин',
        validators=[validate_cooking_time],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата составления рецепта',)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга',
    )
    color = ColorField(
        max_length=7,
        verbose_name='Цветовой код',
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Слаг тэга',
        validators=[RegexValidator(r'^[\w.@+-]+')]
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )

    def __str__(self):
        return f'{self.name}'


class IngredientAmount(models.Model):
    name = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Название ингредиента',
    )
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return (
            f'{self.name.name} - {self.amount}, {self.name.measurement_unit}'
        )


class FollowAuthor(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='added_to_favorite',
        verbose_name='Подписчик',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='added_to_favorite',
        verbose_name='Рецепт',
    )


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='added_to_cart',
        verbose_name='Покупатель',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='added_to_cart',
        verbose_name='Рецепт',
    )

# ############################################################################
# import datetime as dt
# 
# from django.contrib.auth.models import AbstractUser
# from django.core.exceptions import ValidationError
# from django.core.validators import (
#     RegexValidator, MinValueValidator, MaxValueValidator
# )
# from django.db import models
# 
# USER = 'user'
# MODERATOR = 'moderator'
# ADMIN = 'admin'
# 
# ROLES = [
#     (USER, 'user'),
#     (MODERATOR, 'moderator'),
#     (ADMIN, 'admin'),
# ]
# 
# 
# class User(AbstractUser):
#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         verbose_name='Имя пользователя',
#         validators=[RegexValidator(r'^[\w.@+-]+')]
#     )
#     email = models.EmailField(
#         max_length=254,
#         unique=True,
#         verbose_name='Эл. почта'
#     )
#     first_name = models.CharField(
#         max_length=150,
#         blank=True,
#         verbose_name='Имя'
#     )
#     last_name = models.CharField(
#         max_length=150,
#         blank=True,
#         verbose_name='Фамилия'
#     )
#     bio = models.TextField(
#         blank=True,
#         verbose_name='Биография'
#     )
#     role = models.CharField(
#         max_length=100,
#         verbose_name='Роли',
#         default=USER,
#         choices=ROLES,
#     )
#     confirmation_code = models.CharField(
#         max_length=256,
#         blank=True,
#         verbose_name='Код подтверждения'
#     )
# 
#     REQUIRED_FIELDS = ['email']
# 
#     @property
#     def is_admin(self):
#         return self.is_superuser or self.role == ADMIN
# 
#     @property
#     def is_moderator(self):
#         return self.role == MODERATOR
# 
#     @property
#     def is_user(self):
#         return self.role == USER
# 
#     class Meta:
#         ordering = ['id']
# 
#     def __str__(self):
#         return self.username
# 
# 
# class Category(models.Model):
#     name = models.CharField(
#         max_length=256,
#         verbose_name='Название категории',
#     )
#     slug = models.SlugField(
#         unique=True,
#         max_length=50,
#         verbose_name='Слаг категории',
#     )
# 
#     class Meta:
#         ordering = ['id']
# 
#     def __str__(self):
#         return self.name
# 
# 
# class Genre(models.Model):
#     name = models.CharField(
#         max_length=256,
#         verbose_name='Название жанра',
#     )
#     slug = models.SlugField(
#         unique=True,
#         max_length=50,
#         verbose_name='Слаг жанра',
#     )
# 
#     class Meta:
#         ordering = ['id']
# 
#     def __str__(self):
#         return self.name
# 
# 
# def validate_year(value):
#     if value > dt.datetime.now().year:
#         raise ValidationError(
#             'Год выпуска не может быть больше текущего'
#         )
#     return value
# 
# 
# class Title(models.Model):
#     name = models.CharField(
#         'Название',
#         max_length=256,
#         db_index=True,
#     )
#     year = models.IntegerField(
#         'Год выпуска',
#         db_index=True,
#         validators=[validate_year],
#     )
#     description = models.TextField(
#         'Описание',
#         blank=True,
#     )
#     genre = models.ManyToManyField(
#         Genre,
#         through='GenreTitle',
#         verbose_name='Жанр произведения',
#     )
#     category = models.ForeignKey(
#         Category,
#         related_name='title',
#         verbose_name='Категория произведения',
#         on_delete=models.SET_DEFAULT,
#         default='Категория не указана',
#     )
# 
#     class Meta:
#         ordering = ['name']
# 
#     def __str__(self):
#         return self.name
# 
# 
# class GenreTitle(models.Model):
#     genre = models.ForeignKey(
#         Genre,
#         verbose_name='Жанр',
#         on_delete=models.SET_DEFAULT,
#         default='Жанр не указан',
#     )
#     title = models.ForeignKey(
#         Title,
#         verbose_name='Произведение',
#         on_delete=models.CASCADE,
#     )
# 
#     def __str__(self):
#         return f'{self.genre} {self.title}'
# 
# 
# class Review(models.Model):
#     title = models.ForeignKey(
#         Title,
#         on_delete=models.CASCADE,
#         related_name='reviews',
#         verbose_name='Произведение',
#     )
#     text = models.TextField(verbose_name='Текст обзора')
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='reviews',
#     )
#     score = models.PositiveSmallIntegerField(
#         validators=[
#             MinValueValidator(1),
#             MaxValueValidator(10),
#         ],
#         verbose_name='Рейтинг',
#     )
#     pub_date = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='Дата публикации',
#     )
# 
#     class Meta:
#         constraints = [models.UniqueConstraint(
#             fields=['title', 'author'],
#             name='unique_review',
#         )]
#         ordering = ['id']
# 
#     def __str__(self):
#         return self.text
# 
# 
# class Comment(models.Model):
#     review = models.ForeignKey(
#         Review,
#         on_delete=models.CASCADE,
#         related_name='comments',
#         verbose_name='Обзор',
#     )
#     text = models.TextField(verbose_name='Текст комментария')
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comments',
#         verbose_name='Автор комментария',
#     )
#     pub_date = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='Дата публикации',
#     )
# 
#     class Meta:
#         ordering = ['id']
# 
#     def __str__(self):
#         return self.text
# ############################################################################