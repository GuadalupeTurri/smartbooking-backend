
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Sala, Reserva
from .serializers import SalaSerializer, ReservaSerializer


class SalaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sala.objects.filter(activa=True)
    serializer_class = SalaSerializer
    permission_classes = [IsAuthenticated]


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user

        if usuario.rol == 'ADMIN':
            return Reserva.objects.all().order_by('-creada')

        return Reserva.objects.filter(
            usuario=usuario
        ).order_by('-creada')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def update(self, request, *args, **kwargs):
        reserva = self.get_object()

        if reserva.usuario != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                'No podés modificar una reserva de otro usuario.'
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        reserva = self.get_object()

        if reserva.usuario != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                'No podés eliminar una reserva de otro usuario.'
            )

        return super().destroy(request, *args, **kwargs)
