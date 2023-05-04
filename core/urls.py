from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('trainees', views.TraineeViewSet)

urlpatterns = router.urls
