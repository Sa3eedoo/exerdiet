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
        HIGH = 'H', 'High'
        MEDIUM = 'M', 'Medium'
        LOW = 'L', 'Low'
        TRACKED = 'T', 'Track your activity'

    class Goal(models.TextChoices):
        GAIN = 'G', 'Gain weight'
        KEEP = 'K', 'Keep weight'
        LOSE = 'L', 'Lose weight'

    birthdate = models.DateField()
    height = models.DecimalField(max_digits=4, decimal_places=1,
                                 validators=[MinValueValidator(0)])
    weight = models.DecimalField(max_digits=4, decimal_places=1,
                                 validators=[MinValueValidator(0)])
    daily_calories_needs = models.PositiveIntegerField(default=0, blank=True)
    daily_water_needs = models.PositiveIntegerField(default=0, blank=True)
    daily_water_intake = models.PositiveIntegerField(default=0, blank=True)
    # TODO: add defalut value
    carbs_ratio = models.DecimalField(max_digits=2, decimal_places=2,
                                      blank=True,
                                      validators=[MinValueValidator(0), MaxValueValidator(1)])
    # TODO: add defalut value
    fats_ratio = models.DecimalField(max_digits=2, decimal_places=2,
                                     blank=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(1)])
    # TODO: add defalut value
    protein_ratio = models.DecimalField(max_digits=2, decimal_places=2,
                                        blank=True,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    was_active_today = models.BooleanField(default=False, blank=True)
    daily_streak = models.PositiveSmallIntegerField(default=0, blank=True)
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
        return 2500

    def calculate_daily_water_needs(self):
        return 3000

    def save(self, *args, **kwargs):
        if not self.pk and not self.daily_calories_needs:
            self.daily_calories_needs = self.calculate_daily_calories_needs()
        if not self.pk and not self.daily_water_needs:
            self.daily_water_needs = self.calculate_daily_water_needs()
        super().save(*args, **kwargs)
