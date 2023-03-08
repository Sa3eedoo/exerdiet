from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Trainee(models.Model):
    ACTIVITY_LEVEL_HIGH = 'H'
    ACTIVITY_LEVEL_MEDIUM = 'M'
    ACTIVITY_LEVEL_LOW = 'L'
    ACTIVITY_LEVEL_CHOICES = [
        (ACTIVITY_LEVEL_HIGH, 'High'),
        (ACTIVITY_LEVEL_MEDIUM, 'Medium'),
        (ACTIVITY_LEVEL_LOW, 'Low')
    ]

    GOAL_GAIN = 'G'
    GOAL_KEEP = 'K'
    GOAL_LOSE = 'L'
    GOAL_CHOICES = [
        (GOAL_GAIN, 'Gain'),
        (GOAL_KEEP, 'Keep'),
        (GOAL_LOSE, 'Lose')
    ]

    birthdate = models.DateField()
    height = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(400)]
    )
    weight = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(800)]
    )
    calories_needs = models.PositiveIntegerField()
    calories_intake = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    water_intake = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)]
    )
    water_needs = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)]
    )
    carbs_ratio = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )
    fats_ratio = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )
    protein_ratio = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )
    was_active_today = models.BooleanField()
    streak = models.PositiveIntegerField()
    activity_level = models.CharField(max_length=1,
                                      choices=ACTIVITY_LEVEL_CHOICES,
                                      default=ACTIVITY_LEVEL_MEDIUM)
    goal = models.CharField(max_length=1,
                            choices=GOAL_CHOICES,
                            default=GOAL_KEEP)
    image = models.ImageField(upload_to='core/images/trainees')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
