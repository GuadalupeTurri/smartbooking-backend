
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from usuarios.models import Usuario
from .models import Sala, Reserva


class ReservaModelTests(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='usuario_prueba',
            email='prueba@gmail.com',
            password='Prueba123!'
        )

        self.sala = Sala.objects.create(
            nombre='Sala de prueba',
            descripcion='Sala para pruebas automatizadas',
            capacidad=5
        )

        self.inicio = timezone.now() + timedelta(days=1)
        self.fin = self.inicio + timedelta(hours=1)

    def test_reserva_con_horario_valido(self):
        reserva = Reserva(
            usuario=self.usuario,
            sala=self.sala,
            fecha_inicio=self.inicio,
            fecha_fin=self.fin
        )

        reserva.full_clean()

    def test_rechaza_fecha_pasada(self):
        reserva = Reserva(
            usuario=self.usuario,
            sala=self.sala,
            fecha_inicio=timezone.now() - timedelta(days=1),
            fecha_fin=timezone.now() - timedelta(hours=23)
        )

        with self.assertRaises(ValidationError):
            reserva.full_clean()

    def test_rechaza_fecha_fin_anterior_al_inicio(self):
        reserva = Reserva(
            usuario=self.usuario,
            sala=self.sala,
            fecha_inicio=self.inicio,
            fecha_fin=self.inicio - timedelta(minutes=30)
        )

        with self.assertRaises(ValidationError):
            reserva.full_clean()

    def test_rechaza_reservas_superpuestas(self):
        Reserva.objects.create(
            usuario=self.usuario,
            sala=self.sala,
            fecha_inicio=self.inicio,
            fecha_fin=self.fin
        )

        segunda_reserva = Reserva(
            usuario=self.usuario,
            sala=self.sala,
            fecha_inicio=self.inicio + timedelta(minutes=30),
            fecha_fin=self.fin + timedelta(minutes=30)
        )

        with self.assertRaises(ValidationError):
            segunda_reserva.full_clean()

