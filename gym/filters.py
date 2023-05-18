from django_filters import rest_framework as filters
from .models import Exercise, CustomExercise, Workout, PerformedWorkout


class ExerciseFilter(filters.FilterSet):
    class Meta:
        model = Exercise
        fields = {
            'body_part': ['exact'],
            'is_repetitive': ['exact'],
            'calories_burned': ['gte', 'lte'],
        }


class PerformedWorkoutFilter(filters.FilterSet):
    class Meta:
        model = PerformedWorkout
        fields = {
            'time_performed': ['gte', 'lte'],
        }
