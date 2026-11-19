
import copy

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Sala, Reserva


class SalaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sala
        fields = [
            'id',
            'nombre',
            'descripcion',
            'capacidad',
            'activa'
        ]
        read_only_fields = ['id']


class ReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = [
            'id',
            'usuario',
            'sala',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'creada'
        ]
        read_only_fields = [
            'id',
            'usuario',
            'estado',
            'creada'
        ]

    def validate(self, attrs):
        if self.instance:
            reserva = copy.copy(self.instance)
        else:
            reserva = Reserva(
                usuario=self.context['request'].user
            )

        for campo, valor in attrs.items():
            setattr(reserva, campo, valor)

        try:
            reserva.clean()
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages)

        return attrs

