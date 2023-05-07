from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExerciseSerializer
from .models import Exercise
from .filters import ExerciseFilter
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