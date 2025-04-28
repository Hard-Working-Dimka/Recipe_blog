import time

from django.core.management.base import BaseCommand
from recepies.models import Recipe, Order

SLEEP_TIME = 10


def update_recipies():
    while True:

        orders = Order.objects.all()
        for order in orders:
            recipes = Recipe.objects.filter(
                type_of_menu__in=order.type_of_menu.all(),
                food_intake__in=order.food_intake.all()
            ).exclude(
                id__in=order.recipes.values_list('id', flat=True),
            ).order_by('?')

            safe_recipe = recipes.exclude(allergy__in=order.allergy.all()).first()
            if safe_recipe:
                order.recipes.add(safe_recipe)
                order.save()

        time.sleep(SLEEP_TIME)


class Command(BaseCommand):
    help = 'Update_recipies'
    update_recipies()
