from django.urls import path
from . import views

urlpatterns = [
    path('sensors/', views.SensorsView.as_view()),
    path('sensors/<int:pk>/', views.SensorView.as_view()),
    path('measurements/', views.MeasurementView.as_view()),
]
