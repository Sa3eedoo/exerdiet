from rest_framework import serializers
from core.models import Trainee
from .models import Exercise, CustomExercise, Workout, PerformedWorkout, ExerciseInstance

CALORIE_BURNED_LEVEL_LOW = 100
CALORIE_BURNED_LEVEL_HIGH = 250


class ExerciseSerializer(serializers.ModelSerializer):
    calorie_burned_level = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'body_part', 'calories_burned',
                  'is_repetitive', 'calorie_burned_level', 'image']

    def get_calorie_burned_level(self, exercise: Exercise):
        if exercise.calories_burned == 0:
            return 'Zero'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_LOW:
            return 'Low'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_HIGH:
            return 'Medium'
        return 'High'


class CustomExerciseCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomExercise
        fields = ['id', 'name', 'body_part',
                  'calories_burned', 'is_repetitive', 'image']
        read_only_fields = ['id']

    def create(self, validated_data):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)
        custom_exercise = CustomExercise(**validated_data)
        custom_exercise.trainee = trainee
        custom_exercise.save()
        return custom_exercise


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
