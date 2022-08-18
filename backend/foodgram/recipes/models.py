from colorfield.fields import ColorField
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    description = models.TextField()
    ingredients = models.ManyToManyField(
        'IngredientAmount',
#        on_delete=models.CASCADE,
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        'Tag',
#        on_delete=models.CASCADE,
        related_name='recipe',
    )
    cooking_time = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=200)
    color = ColorField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
    )
    amount = models.IntegerField()
    unit = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_unit',
    )

    def __str__(self):
        return self.title


class FollowAuthor(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        null=True,
    )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='added_to_favorite',
        null=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        null=True,
    )


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        null=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
    )
