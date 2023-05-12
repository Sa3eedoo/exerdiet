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
    calories = models.IntegerField(validators=[MinValueValidator(0)])
    carbs = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0)])
    fats = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0)])
    protein = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0)])
    image = models.ImageField(
        upload_to='diet/images/foods', null=True, blank=True)

    def __str__(self) -> str:
        return self.name + ' (' + str(self.calories) + ' cals/100gm)'


class CustomFood(Food):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='custom_foods'
    )

    class Meta:
        db_table = 'diet_custom_food'
        verbose_name = "Custom Food"
        verbose_name_plural = "Custom Foods"

    def __str__(self) -> str:
        return self.name + ' (' + str(self.calories) + ' cals/100gm)' + ' / ' + str(self.trainee)


class Recipe(models.Model):
    name = models.CharField(max_length=150)
    instructions = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='diet/images/recipes', null=True, blank=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='recipes'
    )

    def __str__(self) -> str:
        return self.name + ' (' + str(self.get_total_calories()) + 'cals)' + ' / ' + str(self.trainee)

    def get_total_calories(self):
        total_calories = 0
        for food_instance in self.food_instances.all():
            total_calories += food_instance.get_total_calories()
        return int(total_calories)


class Meal(models.Model):
    name = models.CharField(max_length=150)
    time_eaten = models.DateTimeField(auto_now=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='meals'
    )
    recipes = models.ManyToManyField(Recipe, related_name='meals', blank=True)

    def __str__(self) -> str:
        return self.name + ' (' + str(self.get_total_calories()) + 'cals)' + ' / ' + str(self.trainee) + ' / ' + str(self.time_eaten)

    def get_total_calories(self):
        total_calories = 0
        for recipe in self.recipes.all():
            total_calories += recipe.get_total_calories()
        for food_instance in self.food_instances.all():
            total_calories += food_instance.get_total_calories()
        return int(total_calories)


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
        return self.food.name + ' (' + str(self.quantity) + ' gm/ml)'

    def get_total_calories(self):
        total_calories = 0
        if self.food:
            total_calories += self.food.calories * self.quantity / 100
        return int(total_calories)


class Water(models.Model):
    amount = models.PositiveIntegerField()
    drinking_date = models.DateField(auto_now=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='waters'
    )
