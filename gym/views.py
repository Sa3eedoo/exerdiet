from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from .models import Exercise, CustomExercise
from .serializers import ExerciseSerializer, CustomExerciseSerializer
from .filters import ExerciseFilter, CustomExerciseFilter
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