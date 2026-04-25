from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'gyms', views.GymViewSet, basename='gym')
router.register(r'classes', views.ClassViewSet, basename='gymclass')
router.register(r'plans', views.PlanViewSet, basename='plan')
router.register(r'trainers', views.TrainerViewSet, basename='trainer')

urlpatterns = [
    path('', include(router.urls)),
]
