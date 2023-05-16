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

    def create(self, validated_data):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)
        custom_exercise = CustomExercise(**validated_data)
        custom_exercise.trainee = trainee
        custom_exercise.save()
        return custom_exercise


class SimpleExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'body_part']


class ExerciseInstanceSerializer(serializers.ModelSerializer):
    exercise = SimpleExerciseSerializer(read_only=True)
    total_calories = serializers.SerializerMethodField(read_only=True)

    def get_total_calories(self, exercise_instance: ExerciseInstance):
        return exercise_instance.get_total_calories()

    class Meta:
        model = ExerciseInstance
        fields = ['id', 'exercise', 'duration', 'sets',  'total_calories']


class ExerciseInstanceCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    exercise_id = serializers.IntegerField()

    def validate_exercise_id(self, value):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)

        if not Exercise.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                'No exercise with the given id was found.'
            )
        if Exercise.objects.filter(id=value, customexercise__isnull=False).exists():
            if not CustomExercise.objects.filter(exercise_ptr_id=value, trainee=trainee).exists():
                raise serializers.ValidationError(
                    'No exercise with the given id was found.'
                )
        return value

    class Meta:
        model = ExerciseInstance
        fields = ['id', 'exercise_id', 'duration', 'sets']

    def create(self, validated_data):
        workout_id = self.context['workout_id']
        exercise_instance = ExerciseInstance(workout_id=workout_id,
                                             **validated_data)
        exercise_instance.save()
        return exercise_instance


class ExerciseInstanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseInstance
        fields = ['duration', 'sets']


class WorkoutSerializer(serializers.ModelSerializer):
    exercise_instances = ExerciseInstanceSerializer(many=True, read_only=True)
    total_calories = serializers.SerializerMethodField(read_only=True)

    def get_total_calories(self, workout: Workout):
        return workout.get_total_calories()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'instructions', 'image',
                  'exercise_instances', 'total_calories']

    def create(self, validated_data):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)
        workout = Workout(**validated_data)
        workout.trainee = trainee
        workout.save()
        return workout


class WorkoutUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['name', 'instructions', 'image']


class PerformedWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformedWorkout
        fields = ['id', 'name', 'time_performed',
                  'trainee', 'workouts', 'exercise_instances']
