from rest_framework import serializers
from .models import Exercise, CustomExercise, Workout

class ExerciseSerializer(serializers.ModelSerializer):
    body_part = serializers.CharField(source='get_body_part_display')
    calorie_burned_level = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'body_part', 'calories_burned', 'image', 'is_repetitive', 'calorie_burned_level']
        
    def get_calorie_burned_level(self, exercise: Exercise):
        CALORIE_BURNED_LEVEL_LOW = 100
        CALORIE_BURNED_LEVEL_HIGH = 250
        if exercise.calories_burned == 0:
            return 'Zero'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_LOW:
            return 'Low'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_HIGH:
            return 'Medium'
        return 'High'
    

class CustomExerciseSerializer(serializers.ModelSerializer):
    body_part_display = serializers.CharField(source='get_body_part_display', read_only=True)
    calorie_burned_level = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomExercise
        fields = ['id', 'trainee', 'name', 'body_part', 'body_part_display', 'calories_burned', 'image', 'is_repetitive', 'calorie_burned_level']
        
    def get_calorie_burned_level(self, exercise: CustomExercise):
        CALORIE_BURNED_LEVEL_LOW = 100
        CALORIE_BURNED_LEVEL_HIGH = 250
        if exercise.calories_burned == 0:
            return 'Zero'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_LOW:
            return 'Low'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_HIGH:
            return 'Medium'
        return 'High'
    
    
class WorkoutSerializer(serializers.ModelSerializer):
    performed_workouts_count = serializers.SerializerMethodField()
    trainee_name = serializers.SerializerMethodField()

    def get_trainee_name(self, workout: Workout()):
        return workout.trainee.full_name()

    def get_performed_workouts_count(self, workout: Workout()):
        return workout.performed_workouts.count()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'instructions', 'image', 'trainee', 'trainee_name', 'performed_workouts', 'performed_workouts_count']
        read_only_fields = ['performed_workouts']