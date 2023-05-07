from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('exercises', views.ExerciseViewSet, basename='exercises')

exercises_router = routers.NestedDefaultRouter(
    router, 'exercises', lookup='exercise')

# URLConf
urlpatterns = router.urls + exercises_router.urls