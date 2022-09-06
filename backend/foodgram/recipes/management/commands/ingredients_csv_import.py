import os

from csv import DictReader
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            print('Ingredient data already loaded...exiting.')
            return

        print('Loading Ingredient data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', '..', '..',
            'data', 'ingredients.csv'
        )

        temp_pk = 0
        for row in DictReader(open(path)):
            ingredient = Ingredient(
                pk=temp_pk+1,
                name=row['name'],
                measurement_unit=row['measurement_unit'],
            )
            temp_pk += 1

            ingredient.save()
