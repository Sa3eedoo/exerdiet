from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('trainees', views.TraineeViewSet, basename='trainees')

urlpatterns = router.urls
