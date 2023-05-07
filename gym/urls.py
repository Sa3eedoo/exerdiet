from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('exercises', views.ExerciseViewSet, basename='exercises')
router.register('custom_exercises', views.CustomExerciseViewSet, basename='custom_exercises')
router.register('workouts', views.WorkoutViewSet, basename='workouts')
router.register('performed_workouts', views.PerformedWorkoutViewSet, basename='performed_workouts')

exercises_router = routers.NestedDefaultRouter(
    router, 'exercises', lookup='exercise')

custom_exercises_router = routers.NestedDefaultRouter(
    router, 'custom_exercises', lookup='custom_exercise')

workouts_router = routers.NestedDefaultRouter(
    router, 'workouts', lookup='workout')

performed_workouts_router = routers.NestedDefaultRouter(
    router, 'performed_workouts', lookup='performed_workout')

# URLConf
urlpatterns = router.urls + exercises_router.urls + custom_exercises_router.urls + workouts_router.urls + performed_workouts_router.urls