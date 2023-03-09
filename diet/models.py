from django.db import models
from core.models import Trainee


class Food(models.Model):
    class Category(models.TextChoices):
        FOOD = 'F', 'Food'
        BEVERAGE = 'B', 'Beverage'
        SEASONING = 'S', 'Seasoning'

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=1,
                                choices=Category.choices,
                                default=Category.FOOD)
    calories = models.DecimalField(max_digits=5, decimal_places=1)
    carbs = models.DecimalField(max_digits=5, decimal_places=1)
    fats = models.DecimalField(max_digits=5, decimal_places=1)
    protein = models.DecimalField(max_digits=5, decimal_places=1)
    image = models.ImageField(
        upload_to='diet/images/foods', null=True, blank=True)


class CustomFood(Food):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='custom_foods'
    )

    class Meta:
        db_table = 'diet_custom_food'


class Recipe(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='diet/images/recipes', null=True, blank=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='recipes'
    )
    super_recipes = models.ManyToManyField(
        'self', symmetrical=False, related_name='child_recipes'
    )


class Meal(models.Model):
    name = models.CharField(max_length=150)
    time_eaten = models.DateTimeField(auto_now=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='meals'
    )
    recipes = models.ManyToManyField(Recipe, related_name='meals')


class FoodInstance(models.Model):
    quantity = models.DecimalField(max_digits=5, decimal_places=1)
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, related_name='food_instances'
    )
    recipes = models.ManyToManyField(Recipe, related_name='food_instances')
    meals = models.ManyToManyField(Meal, related_name='food_instances')

    class Meta:
        db_table = 'diet_food_instance'
