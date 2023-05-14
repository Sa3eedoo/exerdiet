from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.username


class Trainee(models.Model):
    class ActivityLevel(models.TextChoices):
        EXTRA = 'E', 'Extra'
        HIGH = 'H', 'High'
        MEDIUM = 'M', 'Medium'
        LOW = 'L', 'Low'
        NONE = 'N', 'None'
        TRACKED = 'T', 'Track your activity'

    class Goal(models.TextChoices):
        GAIN = 'G', 'Gain weight'
        KEEP = 'K', 'Keep weight'
        LOSE = 'L', 'Lose weight'

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    height = models.DecimalField(max_digits=4, decimal_places=1,
                                 validators=[MinValueValidator(0)])
    weight = models.DecimalField(max_digits=4, decimal_places=1,
                                 validators=[MinValueValidator(0)])
    daily_calories_needs = models.IntegerField(
        default=0, blank=True, validators=[MinValueValidator(0)])
    is_daily_calories_needs_custom = models.BooleanField(default=False)
    daily_water_needs = models.IntegerField(
        default=0, blank=True, validators=[MinValueValidator(0)])
    is_daily_water_needs_custom = models.BooleanField(default=False)
    carbs_ratio = models.DecimalField(max_digits=2, decimal_places=2,
                                      default=0.5, blank=True,
                                      validators=[MinValueValidator(0), MaxValueValidator(1)])
    fats_ratio = models.DecimalField(max_digits=2, decimal_places=2,
                                     default=0.2, blank=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(1)])
    protein_ratio = models.DecimalField(max_digits=2, decimal_places=2,
                                        default=0.3, blank=True,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    is_macronutrients_ratios_custom = models.BooleanField(default=False)
    was_active_today = models.BooleanField(default=False, blank=True)
    daily_streak = models.SmallIntegerField(
        default=0, blank=True, validators=[MinValueValidator(0)])
    activity_level = models.CharField(max_length=1,
                                      choices=ActivityLevel.choices,
                                      default=ActivityLevel.MEDIUM,
                                      blank=True)
    goal = models.CharField(max_length=1,
                            choices=Goal.choices,
                            default=Goal.KEEP,
                            blank=True)
    image = models.ImageField(
        upload_to='core/images/trainees', null=True, blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username

    def age(self):
        today = date.today()
        dob = self.birthdate
        years_difference = today.year - dob.year
        is_before_birthday = (today.month, today.day) < (dob.month, dob.day)
        if is_before_birthday:
            years_difference -= 1
        return years_difference

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def calculate_daily_calories_needs(self):
        weight = float(self.weight)
        height = float(self.height)
        age = self.age()
        if self.gender == self.Gender.MALE:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

        if self.activity_level == self.ActivityLevel.TRACKED:
            total_calories = bmr
        elif self.activity_level == self.ActivityLevel.NONE:
            total_calories = bmr * 1.2
        elif self.activity_level == self.ActivityLevel.LOW:
            total_calories = bmr * 1.375
        elif self.activity_level == self.ActivityLevel.MEDIUM:
            total_calories = bmr * 1.55
        elif self.activity_level == self.ActivityLevel.HIGH:
            total_calories = bmr * 1.725
        elif self.activity_level == self.ActivityLevel.EXTRA:
            total_calories = bmr * 1.9

        if self.goal == self.Goal.KEEP:
            return int(total_calories)
        if self.goal == self.Goal.LOSE:
            return int(total_calories * 0.9)
        if self.goal == self.Goal.GAIN:
            return int(total_calories * 1.1)

    def calculate_daily_water_needs(self):
        weight = float(self.weight)
        return 35 * weight

    def get_default_macronutrients_ratios(self):
        return [0.5, 0.2, 0.3]

    def save(self, *args, **kwargs):
        if not self.activity_level:
            self.activity_level = self.ActivityLevel.MEDIUM

        if not self.goal:
            self.goal = self.Goal.KEEP

        if not self.daily_calories_needs or not self.is_daily_calories_needs_custom:
            self.is_daily_calories_needs_custom = False
            self.daily_calories_needs = self.calculate_daily_calories_needs()

        if not self.daily_water_needs or not self.is_daily_water_needs_custom:
            self.is_daily_water_needs_custom = False
            self.daily_water_needs = self.calculate_daily_water_needs()

        if (not self.carbs_ratio and not self.fats_ratio and not self.protein_ratio) or not self.is_macronutrients_ratios_custom:
            self.is_macronutrients_ratios_custom = False
            self.carbs_ratio, self.fats_ratio, self.protein_ratio = self.get_default_macronutrients_ratios()

        if self.daily_streak == None:
            self.daily_streak = 0

        super().save(*args, **kwargs)
