from django.db import models
from django.conf import settings

TIPO_USUARIO = (('AD', 'administrador'),('CA','cliente de app'))

class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(choices=TIPO_USUARIO, max_length=2, null=False, blank=False)
    id_strava = models.CharField(max_length=100, null=True, blank=True)
# Create your models here.
