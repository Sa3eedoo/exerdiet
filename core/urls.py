from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('trainees', views.TraineeViewSet, basename='trainees')

urlpatterns = [
    path('', include(router.urls)),
    path('activate/<uid>/<token>/', views.activate_user),
    path('password/reset/confirm/<uid>/<token>/', views.reset_password)
]
