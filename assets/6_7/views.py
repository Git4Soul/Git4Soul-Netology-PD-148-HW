from rest_framework import viewsets, permissions, throttling
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadOnly


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_throttles(self):
        """Троттлинг"""
        if self.request.user.is_authenticated:
            self.throttle_classes = [throttling.UserRateThrottle]
        else:
            self.throttle_classes = [throttling.AnonRateThrottle]
        return super().get_throttles()

    def perform_create(self, serializer):
        """Автоматическая установка создателя"""
        serializer.save(creator=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Проверка прав при удалении"""
        instance = self.get_object()
        if instance.creator != request.user:
            return Response({'detail': 'Вы не можете удалить это объявление.'}, status=403)
        self.perform_destroy(instance)
        return Response(status=204)