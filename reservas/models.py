
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    capacidad = models.PositiveIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    sala = models.ForeignKey(
        Sala,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    estado = models.CharField(
        max_length=12,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )

    creada = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.utils import timezone

        # RN02: no permitir fechas pasadas
        if self.fecha_inicio and self.fecha_inicio < timezone.now():
            raise ValidationError(
                'No se pueden realizar reservas en fechas pasadas.'
            )

        # RN03: la finalización debe ser posterior al inicio
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    'La fecha de finalización debe ser posterior al inicio.'
                )

        # RN01: evitar reservas superpuestas en la misma sala
        # Las reservas canceladas no bloquean horarios
        if (
            self.estado != self.Estado.CANCELADA
            and self.sala_id
            and self.fecha_inicio
            and self.fecha_fin
        ):
            reservas_existentes = Reserva.objects.filter(
                sala=self.sala,
                fecha_inicio__lt=self.fecha_fin,
                fecha_fin__gt=self.fecha_inicio
            ).exclude(
                estado=Reserva.Estado.CANCELADA
            )

            if self.pk:
                reservas_existentes = reservas_existentes.exclude(
                    pk=self.pk
                )

            if reservas_existentes.exists():
                raise ValidationError(
                    'La sala ya tiene una reserva en ese horario.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.sala.nombre} - {self.usuario.username}'

