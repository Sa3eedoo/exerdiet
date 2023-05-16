from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from core.models import Trainee
from core.permissions import IsAuthenticatedAndTrainee
from .models import Exercise, CustomExercise, ExerciseInstance, Workout, PerformedWorkout
from .filters import ExerciseFilter, CustomExerciseFilter, WorkoutFilter, PerformedWorkoutFilter
from . import serializers


class ExerciseViewSet(ReadOnlyModelViewSet):
    queryset = Exercise.objects.\
        filter(customexercise__isnull=True).order_by('name')
    serializer_class = serializers.ExerciseSerializer
    permission_classes = [IsAuthenticatedAndTrainee]

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = ExerciseFilter


class CustomExerciseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedAndTrainee]
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = CustomExerciseFilter

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = Trainee.objects.get(user_id=user_id)
        return CustomExercise.objects.filter(trainee=trainee).order_by('name')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return serializers.CustomExerciseCreateUpdateSerializer
        return serializers.ExerciseSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def destroy(self, request, *args, **kwargs):
        custom_exercise = self.get_object()
        if custom_exercise.exercise_instances.exists():
            return Response({'error': 'Exercise cannot be deleted because it is associated with a workout.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(custom_exercise)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkoutViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticatedAndTrainee]

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = WorkoutFilter

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = Trainee.objects.get(user_id=user_id)
        return Workout.objects.\
            filter(trainee=trainee).\
            prefetch_related('exercise_instances__exercise').\
            order_by('name')

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.WorkoutUpdateSerializer
        return serializers.WorkoutSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def destroy(self, request, *args, **kwargs):
        workout = self.get_object()
        if workout.performed_workouts.exists():
            return Response({'error': 'Workout cannot be deleted because it is associated with a performed workout.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(workout)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkoutExerciseInstanceViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        workout_id = self.kwargs['workout_pk']
        return ExerciseInstance.objects\
            .filter(workout_id=workout_id)\
            .select_related('exercise')\
            .order_by('id')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ExerciseInstanceCreateSerializer
        if self.request.method == 'PATCH':
            return serializers.ExerciseInstanceUpdateSerializer
        return serializers.ExerciseInstanceSerializer

    def get_serializer_context(self):
        return {'workout_id': self.kwargs['workout_pk'],
                'user_id': self.request.user.id}


class PerformedWorkoutViewSet(ModelViewSet):
    serializer_class = serializers.PerformedWorkoutSerializer
    permission_classes = [IsAuthenticatedAndTrainee]

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = PerformedWorkoutFilter

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = Trainee.objects.get(user_id=user_id)
        return PerformedWorkout.objects.filter(trainee=trainee).order_by('name')
