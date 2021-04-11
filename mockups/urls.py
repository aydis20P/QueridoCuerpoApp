from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name="principal"),
    path('resumen-usuario', views.resumen_usuario, name="resumen-usuario"),
    path('resumen-usuario-strava', views.resumen_usuario_strava, name="resumen-usuario-strava"),
    path('calendario-citas', views.calendario_citas, name="calendario-citas"),
    path('citas-disponibles', views.citas_disponibles, name="citas_disponibles"),
    path('alimentacion', views.alimentacion, name="alimentacion"),
]
