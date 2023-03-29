from django.core.validators import MinValueValidator
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
    calories = models.DecimalField(
        max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    carbs = models.DecimalField(
        max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    fats = models.DecimalField(
        max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    protein = models.DecimalField(
        max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    image = models.ImageField(
        upload_to='diet/images/foods', null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class CustomFood(Food):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='custom_foods'
    )

    class Meta:
        db_table = 'diet_custom_food'
        verbose_name = "Custom Food"
        verbose_name_plural = "Custom Foods"

    def __str__(self) -> str:
        return self.name + ' / ' + str(self.trainee)


class Recipe(models.Model):
    name = models.CharField(max_length=150)
    instructions = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='diet/images/recipes', null=True, blank=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='recipes'
    )

    def __str__(self) -> str:
        return self.name + ' / ' + str(self.trainee)


class Meal(models.Model):
    name = models.CharField(max_length=150)
    time_eaten = models.DateTimeField(auto_now=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='meals'
    )
    recipes = models.ManyToManyField(Recipe, related_name='meals', blank=True)

    def __str__(self) -> str:
        return self.name + ' / ' + str(self.trainee) + ' / ' + str(self.time_eaten)


class FoodInstance(models.Model):
    quantity = models.DecimalField(
        max_digits=5, decimal_places=1, validators=[MinValueValidator(1)])
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, related_name='food_instances'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='food_instances', null=True, blank=True
    )
    meal = models.ForeignKey(
        Meal, on_delete=models.CASCADE, related_name='food_instances', null=True, blank=True
    )

    class Meta:
        db_table = 'diet_food_instance'
        verbose_name = "Food Instance"
        verbose_name_plural = "Food Instances"

    def __str__(self) -> str:
        return self.food.name + ' (' + str(self.quantity) + 'gm/ml)'
