from django.db import models

from core.models import Trainee


class Exercise(models.Model):
    class BodyPart(models.TextChoices):
        CHEST = 'CH', 'Chest'
        BACk = 'BK', 'Back'
        ARMS = 'AR', 'Arms'
        LEGS = 'LG', 'Legs'
        CARDIO = 'CR', 'Cardio'
        SHOULDERS = 'SH', 'Shoulders'
        ABS = 'AB', 'Abs'

    name = models.CharField(max_length=150)
    body_part = models.CharField(max_length=2,
                                 choices=BodyPart.choices)
    calories_burned = models.DecimalField(max_digits=5, decimal_places=1)
    is_repetitive = models.BooleanField()

    image = models.ImageField(
        upload_to='gym/images/exercises', null=True, blank=True)


class CustomExercise(Exercise):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='custom_exercises'
    )

    class Meta:
        db_table = 'gym_custom_exercise'


class Workout(models.Model):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='custom_exercises'
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(
        upload_to='gym/images/workouts', null=True, blank=True)


class PerformedWorkout(models.Model):

    time_performed = models.DateTimeField(auto_now=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='performed_workouts'
    )

    class Meta:
        db_table = 'gym_performed_workout'


class ExerciseInstance(models.Model):
    duration = models.PositiveBigIntegerField()
    sets = models.PositiveSmallIntegerField()
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name='exercise_instances'
    )
    workouts = models.ManyToManyField(
        Workout, related_name='exercise_instances')
    performed_workouts = models.ManyToManyField(
        PerformedWorkout, related_name='exercise_instances')
