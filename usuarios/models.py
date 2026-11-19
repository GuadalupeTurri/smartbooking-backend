from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        USUARIO = 'USUARIO', 'Usuario'

    email = models.EmailField(unique=True)
    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.USUARIO
    )

    def __str__(self):
        return self.username
