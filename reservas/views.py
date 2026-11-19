
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Sala, Reserva
from .serializers import SalaSerializer, ReservaSerializer


class SalaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sala.objects.filter(activa=True)
    serializer_class = SalaSerializer
    permission_classes = [IsAuthenticated]


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def es_administrador(self):
        usuario = self.request.user
        return usuario.is_superuser or usuario.rol == 'ADMIN'

    def get_queryset(self):
        usuario = self.request.user

        if self.es_administrador():
            return Reserva.objects.all().order_by('-creada')

        return Reserva.objects.filter(
            usuario=usuario
        ).order_by('-creada')

    def perform_create(self, serializer):
        if self.es_administrador():
            raise PermissionDenied(
                'El administrador no puede crear reservas.'
            )

        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        if self.es_administrador():
            raise PermissionDenied(
                'El administrador no puede modificar reservas.'
            )

        if serializer.instance.usuario != self.request.user:
            raise PermissionDenied(
                'No podés modificar una reserva de otro usuario.'
            )

        serializer.save()

    def perform_destroy(self, instance):
        if self.es_administrador():
            raise PermissionDenied(
                'El administrador no puede cancelar reservas.'
            )

        if instance.usuario != self.request.user:
            raise PermissionDenied(
                'No podés cancelar una reserva de otro usuario.'
            )

        instance.estado = Reserva.Estado.CANCELADA
        instance.save(update_fields=['estado'])
