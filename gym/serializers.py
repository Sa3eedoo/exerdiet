from rest_framework import serializers
from .models import Exercise, CustomExercise, Workout, PerformedWorkout, ExerciseInstance


class ExerciseSerializer(serializers.ModelSerializer):
    body_part = serializers.CharField(source='get_body_part_display')
    calorie_burned_level = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'body_part', 'calories_burned',
                  'image', 'is_repetitive', 'calorie_burned_level']

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
    body_part_display = serializers.CharField(source='get_body_part_display',
                                              read_only=True)
    calorie_burned_level = serializers.SerializerMethodField()

    class Meta:
        model = CustomExercise
        fields = ['id', 'trainee', 'name', 'body_part', 'body_part_display',
                  'calories_burned', 'image', 'is_repetitive', 'calorie_burned_level']

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


class ExerciseInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseInstance
        fields = '__all__'


class WorkoutSerializer(serializers.ModelSerializer):
    performed_workouts_count = serializers.SerializerMethodField()
    trainee_name = serializers.SerializerMethodField()
    exercise_instances = ExerciseInstanceSerializer(many=True)

    def get_trainee_name(self, workout: Workout()):
        return workout.trainee.full_name()

    def get_performed_workouts_count(self, workout: Workout()):
        return workout.performed_workouts.count()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'instructions', 'image', 'exercise_instances',
                  'trainee', 'trainee_name', 'performed_workouts', 'performed_workouts_count']
        read_only_fields = ['performed_workouts']

    def create(self, validated_data):
        exercise_instances = validated_data.pop('exercise_instances')
        workout = Workout.objects.create(**validated_data)
        for exercise_instance in exercise_instances:
            ExerciseInstance.objects.create(workout=workout,
                                            **exercise_instance)
        return workout


class PerformedWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformedWorkout
        fields = ['id', 'name', 'time_performed',
                  'trainee', 'workouts', 'exercise_instances']
