from django.db import models
from core.models import Trainee


class Food(models.Model):
    CATEGORY_FOOD = 'F'
    CATEGORY_BEVERAGE = 'B'
    CATEGORY_SEASONING = 'S'
    CATEGORY_CHOICES = [
        (CATEGORY_FOOD, 'Food'),
        (CATEGORY_BEVERAGE, 'Beverage'),
        (CATEGORY_SEASONING, 'Seasoning')
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=1,
                                choices=CATEGORY_CHOICES,
                                default=CATEGORY_FOOD)
    calories = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    protein = models.IntegerField()
    # image =


class CustomFood(Food):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)


class Recipe(models.Model):
    name = models.CharField(max_length=150)
    instructions = models.TextField()
    # image =
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    super_recipe = models.ManyToManyField(
        'self', symmetrical=False, related_name='recipes'
    )


class Meal(models.Model):
    name = models.CharField(max_length=150)
    time_eaten = models.DateTimeField(auto_now=True)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, related_name='meals')


class FoodInstance(models.Model):
    portion = models.IntegerField()
    food = models.OneToOneField(Food, on_delete=models.PROTECT)
    recipes = models.ManyToManyField(Recipe, related_name='foodinstances')
    meals = models.ManyToManyField(Meal, related_name='foodinstances')
