from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from core.models import Trainee
from core.permissions import IsAuthenticatedAndTrainee
from .models import Exercise, CustomExercise, Workout, PerformedWorkout
from .filters import ExerciseFilter, CustomExerciseFilter, WorkoutFilter, PerformedWorkoutFilter
from . import serializers


class ExerciseViewSet(ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = serializers.ExerciseSerializer

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = ExerciseFilter

    permission_classes = [IsAuthenticatedAndTrainee]


class CustomExerciseViewSet(ModelViewSet):
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = CustomExerciseFilter

    permission_classes = [IsAuthenticatedAndTrainee]

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = Trainee.objects.get(user_id=user_id)
        return CustomExercise.objects.filter(trainee=trainee).all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.CustomExerciseUpdateSerializer
        return serializers.CustomExerciseSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.exercise_instances.exists():
            return Response({'error': 'Exercise cannot be deleted because it is associated with a workout.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkoutViewSet(ModelViewSet):
    serializer_class = serializers.WorkoutSerializer

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = WorkoutFilter

    permission_classes = [IsAuthenticatedAndTrainee]

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = Trainee.objects.get(user_id=user_id)
        return Workout.objects.filter(trainee=trainee).all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.performed_workouts.exists():
            return Response({'error': 'Workout cannot be deleted because it is associated with a performed workout.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PerformedWorkoutViewSet(ModelViewSet):
    serializer_class = serializers.PerformedWorkoutSerializer

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = PerformedWorkoutFilter

    permission_classes = [IsAuthenticatedAndTrainee]

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = Trainee.objects.get(user_id=user_id)
        return PerformedWorkout.objects.filter(trainee=trainee).all()
