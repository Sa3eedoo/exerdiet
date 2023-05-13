from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from .models import Exercise, CustomExercise, Workout, PerformedWorkout
from .serializers import ExerciseSerializer, CustomExerciseSerializer, WorkoutSerializer, PerformedWorkoutSerializer
from .filters import ExerciseFilter, CustomExerciseFilter, WorkoutFilter, PerformedWorkoutFilter
from .pagination import DefaultPagination


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExerciseFilter
    pagination_class = DefaultPagination
    http_method_names = ['get', 'head']

    def get_serializer_context(self):
        return {'request': self.request}
    # search_fields
    # ordering_fields


class CustomExerciseViewSet(viewsets.ModelViewSet):
    queryset = CustomExercise.objects.all()
    serializer_class = CustomExerciseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CustomExerciseFilter
    pagination_class = DefaultPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.exercise_instances.exists():
            return Response({'error': 'Exercise cannot be deleted because it is associated with a workout.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = WorkoutFilter
    pagination_class = DefaultPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.performed_workouts.exists():
            return Response({'error': 'Workout cannot be deleted because it is associated with a performed workout.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PerformedWorkoutViewSet(viewsets.ModelViewSet):
    queryset = PerformedWorkout.objects.all()
    serializer_class = PerformedWorkoutSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PerformedWorkoutFilter
    pagination_class = DefaultPagination
