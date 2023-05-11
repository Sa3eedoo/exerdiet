from django.core.validators import MinValueValidator
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
                                 choices=BodyPart.choices,
                                 default=BodyPart.CARDIO)
    calories_burned = models.IntegerField(validators=[MinValueValidator(0)])
    is_repetitive = models.BooleanField()

    image = models.ImageField(
        upload_to='gym/images/exercises', null=True, blank=True)

    def __str__(self) -> str:
        return self.name + ' (' + str(self.calories_burned) + 'cals/(60sec or 1rep))'


class CustomExercise(Exercise):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='custom_exercises'
    )

    class Meta:
        db_table = 'gym_custom_exercise'
        verbose_name = "Custom Exercise"
        verbose_name_plural = "Custom Exercises"

    def __str__(self) -> str:
        return self.name + ' / ' + str(self.trainee)


class Workout(models.Model):
    name = models.CharField(max_length=150)
    instructions = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='gym/images/workouts', null=True, blank=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='workouts'
    )

    def __str__(self) -> str:
        return self.name + ' / ' + str(self.trainee)


class PerformedWorkout(models.Model):
    name = models.CharField(max_length=150)
    time_performed = models.DateTimeField(auto_now=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='performed_workouts'
    )
    workouts = models.ManyToManyField(
        Workout, related_name='performed_workouts'
    )

    def __str__(self) -> str:
        return self.name + ' / ' + str(self.trainee) + ' / ' + str(self.time_performed)


class ExerciseInstance(models.Model):
    duration = models.PositiveIntegerField()
    sets = models.PositiveSmallIntegerField()
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name='exercise_instances'
    )
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name='exercise_instances', null=True, blank=True
    )
    performed_workout = models.ForeignKey(
        PerformedWorkout, on_delete=models.CASCADE, related_name='exercise_instances', null=True, blank=True
    )

    class Meta:
        db_table = 'gym_exercise_instance'
        verbose_name = "Exercise Instance"
        verbose_name_plural = "Exercises Instance"

    def __str__(self) -> str:
        return self.exercise.name + ' (' + str(self.sets) + ')'
