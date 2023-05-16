from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('exercises', views.ExerciseViewSet)
router.register('custom_exercises',
                views.CustomExerciseViewSet,
                basename='custom_exercises')
router.register('workouts', views.WorkoutViewSet, basename='workouts')
router.register('performed_workouts',
                views.PerformedWorkoutViewSet,
                basename='performed_workouts')

workouts_router = routers.NestedDefaultRouter(router,
                                              'workouts',
                                              lookup='workout')
workouts_router.register('exercise_instances',
                         views.WorkoutExerciseInstanceViewSet,
                         basename='workouts-exercise_instances')

performed_workouts_router = routers.NestedDefaultRouter(router,
                                                        'performed_workouts',
                                                        lookup='performed_workout')
performed_workouts_router.register('workouts',
                                   views.PerformedWorkoutWorkoutViewSet,
                                   basename='performed_workouts-workouts')
performed_workouts_router.register('exercise_instances',
                                   views.PerformedWorkoutExerciseInstanceViewSet,
                                   basename='performed_workouts-exercise_instances')

# URLConf
urlpatterns = router.urls + workouts_router.urls + performed_workouts_router.urls
