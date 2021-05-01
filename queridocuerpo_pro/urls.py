from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name="principal"),
    path('resumen-usuario', views.resumen_usuario, name="resumen-usuario")
]
