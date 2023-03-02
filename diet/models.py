from django.db import models


class food(models.Model):
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
    # image =
    calories = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    protein = models.IntegerField()


class custom_food(food):
    # trainee =
    pass


class recipe(models.Model):
    # trainee =
    name = models.CharField(max_length=150)
    instructions = models.TextField()
    # image =


class meal(models.Model):
    # trainee =
    name = models.CharField(max_length=150)
    time_eaten = models.DateTimeField(auto_now=True)
