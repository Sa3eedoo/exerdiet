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

    class Goal(models.TextChoices):
        GAIN = 'G', 'Gain'
        KEEP = 'K', 'Keep'
        LOSE = 'L', 'Lose'

    birthdate = models.DateField()
    height = models.DecimalField(max_digits=4, decimal_places=1)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    daily_calories_needs = models.PositiveIntegerField()
    daily_calories_intake = models.PositiveIntegerField()
    daily_water_intake = models.PositiveIntegerField()
    daily_water_needs = models.PositiveIntegerField()
    carbs_ratio = models.DecimalField(max_digits=2, decimal_places=2)
    fats_ratio = models.DecimalField(max_digits=2, decimal_places=2)
    protein_ratio = models.DecimalField(max_digits=2, decimal_places=2)
    was_active_today = models.BooleanField(default=False)
    daily_streak = models.PositiveSmallIntegerField(default=0)
    activity_level = models.CharField(max_length=1,
                                      choices=ActivityLevel.choices,
                                      default=ActivityLevel.MEDIUM)
    goal = models.CharField(max_length=1,
                            choices=Goal.choices,
                            default=Goal.KEEP)
    image = models.ImageField(
        upload_to='core/images/trainees', null=True, blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
