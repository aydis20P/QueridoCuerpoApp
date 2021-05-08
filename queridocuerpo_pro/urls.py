from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name="principal"),
    path('resumen-usuario', views.resumen_usuario, name="resumen-usuario"),
    path('perfil-profesional', views.perfil_profesional, name="perfil-profesional"),
    path('perfil-miembro', views.perfil_miembro, name="perfil-miembro"),
    path('plan-alimenticio-miembro', views.plan_alimenticio_miembro, name="plan-alimenticio-miembro"),
    path('resumen-usuario-administrativo', views.resumen_usuario_administrativo, name="resumen-usuario-administrativo"),
]
