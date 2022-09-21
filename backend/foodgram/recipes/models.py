from colorfield.fields import ColorField
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


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
        on_delete=models.SET(deleted_user_id),
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

    def __str__(self):
        return (f'{self.user.username} following {self.author.username}')


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

    def __str__(self):
        return (f'{self.user.username} favorited {self.recipe.name}')


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

    def __str__(self):
        return (f'{self.user.username} added {self.recipe.name} to cart')
