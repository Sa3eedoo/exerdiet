from django_filters import rest_framework as filters
from .models import Exercise, CustomExercise, Workout

class ExerciseFilter(filters.FilterSet):
    
    FILTER_ZERO = '0'
    FILTER_LOW = 'low'
    FILTER_MED = 'medium'
    FILTER_HIGH = 'high'

    calorie_burned_level = filters.ChoiceFilter(
        label='Calorie Burned Level',
        choices=(
            (FILTER_ZERO, 'Zero'),
            (FILTER_LOW, 'Low'),
            (FILTER_MED, 'Medium'),
            (FILTER_HIGH, 'High')
        ),
        method='filter_calorie_burned_level'
    )

    def filter_calorie_burned_level(self, queryset, name, value):
        CALORIE_BURNED_LEVEL_LOW = 100
        CALORIE_BURNED_LEVEL_HIGH = 250
        if value == self.FILTER_ZERO:
            return queryset.filter(calories_burned=0)
        elif value == self.FILTER_LOW:
            return queryset.filter(calories_burned__lt=CALORIE_BURNED_LEVEL_LOW)
        elif value == self.FILTER_MED:
            return queryset.filter(calories_burned__gte=CALORIE_BURNED_LEVEL_LOW, calories_burned__lt=CALORIE_BURNED_LEVEL_HIGH)
        elif value == self.FILTER_HIGH:
            return queryset.filter(calories_burned__gte=CALORIE_BURNED_LEVEL_HIGH)
        else:
            return queryset

    class Meta:
        model = Exercise
        fields = {
            'name': ['exact', 'icontains'],
            'body_part': ['exact'],
            'calories_burned': ['exact', 'gte', 'lte'],
            'is_repetitive': ['exact'],
        }
        
        
class CustomExerciseFilter(filters.FilterSet):
    FILTER_ZERO = '0'
    FILTER_LOW = 'low'
    FILTER_MED = 'medium'
    FILTER_HIGH = 'high'

    calorie_burned_level = filters.ChoiceFilter(
        label='Calorie Burned Level',
        choices=(
            (FILTER_ZERO, 'Zero'),
            (FILTER_LOW, 'Low'),
            (FILTER_MED, 'Medium'),
            (FILTER_HIGH, 'High')
        ),
        method='filter_calorie_burned_level'
    )

    def filter_calorie_burned_level(self, queryset, name, value):
        CALORIE_BURNED_LEVEL_LOW = 100
        CALORIE_BURNED_LEVEL_HIGH = 250
        if value == self.FILTER_ZERO:
            return queryset.filter(calories_burned=0)
        elif value == self.FILTER_LOW:
            return queryset.filter(calories_burned__lt=CALORIE_BURNED_LEVEL_LOW)
        elif value == self.FILTER_MED:
            return queryset.filter(calories_burned__gte=CALORIE_BURNED_LEVEL_LOW, calories_burned__lt=CALORIE_BURNED_LEVEL_HIGH)
        elif value == self.FILTER_HIGH:
            return queryset.filter(calories_burned__gte=CALORIE_BURNED_LEVEL_HIGH)
        else:
            return queryset
    
    class Meta:
        model = CustomExercise
        fields = {
            'name': ['exact', 'icontains'],
            'body_part': ['exact'],
            'calories_burned': ['exact', 'gte', 'lte'],
            'is_repetitive': ['exact'],
            'trainee': ['exact'],
        }
        
        
class WorkoutFilter(filters.FilterSet):
    class Meta:
        model = Workout
        fields = {
            'name': ['exact', 'icontains'],
            'trainee': ['exact'],
            'performed_workouts': ['exact']
        }