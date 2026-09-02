from rest_framework import generics
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer

class SensorsView(generics.ListCreateAPIView):
    """
    GET: Получить список всех датчиков.
    POST: Создать новый датчик.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorView(generics.RetrieveUpdateAPIView):
    """
    GET: Получить информацию по конкретному датчику (включая все его измерения).
    PATCH: Обновить название или описание датчика.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementView(generics.CreateAPIView):
    """
    POST: Добавить новое измерение для датчика.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer