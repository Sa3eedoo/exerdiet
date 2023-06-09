from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime, date
from core.models import Trainee
from core.validators import validate_image_size


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
        max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    fats = models.DecimalField(
        max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    protein = models.DecimalField(
        max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    image = models.ImageField(
        upload_to='diet/images/foods', null=True, blank=True, validators=[validate_image_size])

    def __str__(self) -> str:
        food_str = self.name + ' (' + str(self.calories) + ' cals/'
        if self.category == self.Category.FOOD:
            food_str += '100gm)'
        elif self.category == self.Category.BEVERAGE:
            food_str += '100ml)'
        else:
            food_str += '1tsp)'
        return food_str


class CustomFood(Food):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='custom_foods'
    )

    class Meta:
        db_table = 'diet_custom_food'
        verbose_name = "Custom Food"
        verbose_name_plural = "Custom Foods"

    def __str__(self) -> str:
        custom_food_str = self.name + ' (' + str(self.calories) + ' cals/'
        if self.category == self.Category.FOOD:
            custom_food_str += '100gm)'
        elif self.category == self.Category.BEVERAGE:
            custom_food_str += '100ml)'
        else:
            custom_food_str += '1tsp)'
        custom_food_str += ' / ' + str(self.trainee)
        return custom_food_str


class Recipe(models.Model):
    name = models.CharField(max_length=150)
    instructions = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='diet/images/recipes', null=True, blank=True, validators=[validate_image_size])
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

    def get_total_carbs(self):
        total_carbs = 0
        for food_instance in self.food_instances.all():
            total_carbs += food_instance.get_total_carbs()
        return round(total_carbs, 1)

    def get_total_fats(self):
        total_fats = 0
        for food_instance in self.food_instances.all():
            total_fats += food_instance.get_total_fats()
        return round(total_fats, 1)

    def get_total_protein(self):
        total_protein = 0
        for food_instance in self.food_instances.all():
            total_protein += food_instance.get_total_protein()
        return round(total_protein, 1)


class Meal(models.Model):
    name = models.CharField(max_length=150)
    time_eaten = models.DateTimeField(auto_now_add=True)
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

    def get_total_carbs(self):
        total_carbs = 0
        for recipe in self.recipes.all():
            total_carbs += recipe.get_total_carbs()
        for food_instance in self.food_instances.all():
            total_carbs += food_instance.get_total_carbs()
        return round(total_carbs, 1)

    def get_total_fats(self):
        total_fats = 0
        for recipe in self.recipes.all():
            total_fats += recipe.get_total_fats()
        for food_instance in self.food_instances.all():
            total_fats += food_instance.get_total_fats()
        return round(total_fats, 1)

    def get_total_protein(self):
        total_protein = 0
        for recipe in self.recipes.all():
            total_protein += recipe.get_total_protein()
        for food_instance in self.food_instances.all():
            total_protein += food_instance.get_total_protein()
        return round(total_protein, 1)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = 'Meal @ ' + str(datetime.today())
        super().save(*args, **kwargs)


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
        food_instance_str = self.food.name + ' (' + str(self.quantity)
        if self.food.category == self.food.Category.FOOD:
            food_instance_str += ' gm)'
        elif self.food.category == self.food.Category.BEVERAGE:
            food_instance_str += ' ml)'
        else:
            food_instance_str += ' tsp)'
        return food_instance_str

    def get_total_calories(self):
        total_calories = 0
        if self.food:
            if self.food.category == self.food.Category.SEASONING:
                total_calories += self.food.calories * self.quantity
            total_calories += self.food.calories * self.quantity / 100
        return int(total_calories)

    def get_total_carbs(self):
        total_carbs = 0
        if self.food:
            total_carbs += self.food.carbs * self.quantity / 100
        return round(total_carbs, 1)

    def get_total_fats(self):
        total_fats = 0
        if self.food:
            total_fats += self.food.fats * self.quantity / 100
        return round(total_fats, 1)

    def get_total_protein(self):
        total_protein = 0
        if self.food:
            total_protein += self.food.protein * self.quantity / 100
        return round(total_protein, 1)


class Water(models.Model):
    amount = models.PositiveIntegerField()
    drinking_date = models.DateField()
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='waters'
    )

    def save(self, *args, **kwargs):
        if not self.drinking_date:
            self.drinking_date = date.today()
        super().save(*args, **kwargs)
