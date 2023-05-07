from rest_framework import serializers
from .models import Exercise

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