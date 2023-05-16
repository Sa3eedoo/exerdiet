from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from core.models import Trainee

from ratings.models import Rating


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
        temp = '10rep' if self.is_repetitive else '60sec'
        return self.name + ' (' + str(self.calories_burned) + 'cals/' + temp + ')'


class CustomExercise(Exercise):
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='custom_exercises'
    )

    class Meta:
        db_table = 'gym_custom_exercise'
        verbose_name = "Custom Exercise"
        verbose_name_plural = "Custom Exercises"

    def __str__(self) -> str:
        temp = '10rep' if self.is_repetitive else '60sec'
        return self.name + ' (' + str(self.calories_burned) + 'cals/' + temp + ')' + ' / ' + str(self.trainee)


class Workout(models.Model):
    name = models.CharField(max_length=150)
    instructions = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='gym/images/workouts', null=True, blank=True)
    trainee = models.ForeignKey(
        Trainee, on_delete=models.CASCADE, related_name='workouts'
    )
    ratings = GenericRelation(Rating) # queryset 
    
    def calculate_ratings_count(self):
        return self.ratings.all().count()

    def __str__(self) -> str:
        return self.name + ' (' + str(self.get_total_calories()) + 'cals)' + ' / ' + str(self.trainee)

    def get_total_calories(self):
        total_calories = 0
        for exercise_instance in self.exercise_instances.all():
            total_calories += exercise_instance.get_total_calories()
        return int(total_calories)


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
        return self.name + ' (' + str(self.get_total_calories()) + 'cals)' + ' / ' + str(self.trainee) + ' / ' + str(self.time_performed)

    def get_total_calories(self):
        total_calories = 0
        for workout in self.workouts.all():
            total_calories += workout.get_total_calories()
        for exercise_instance in self.exercise_instances.all():
            total_calories += exercise_instance.get_total_calories()
        return int(total_calories)


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

    def get_total_calories(self):
        total_calories = 0
        if self.exercise:
            if self.exercise.is_repetitive:
                total_calories += (self.exercise.calories_burned *
                                   self.duration * self.sets / 10)
            else:
                total_calories += (self.exercise.calories_burned *
                                   self.duration * self.sets / 60)
        return int(total_calories)
