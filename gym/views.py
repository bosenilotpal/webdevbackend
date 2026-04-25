from rest_framework import viewsets

from .models import Class, Gym, Plans, Trainer
from .serializers import (
    ClassSerializer,
    GymSerializer,
    PlanSerializer,
    TrainerSerializer,
)


class GymViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GymSerializer
    queryset = Gym.objects.select_related('owner_user_id').all()


class ClassViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClassSerializer
    queryset = Class.objects.select_related('gym_id').all()


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plans.objects.select_related('gym_id').prefetch_related('classes').all()


class TrainerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TrainerSerializer
    queryset = Trainer.objects.select_related('gym_id').all()
