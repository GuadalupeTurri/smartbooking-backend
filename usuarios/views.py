
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    RegistroSerializer,
    PerfilSerializer,
    AdminUsuarioSerializer
)


Usuario = get_user_model()


class SoloAdministrador(BasePermission):
    def has_permission(self, request, view):
        usuario = request.user

        return (
            usuario.is_authenticated
            and (usuario.is_superuser or usuario.rol == 'ADMIN')
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class RegistroView(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]


class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error': 'Se requiere el refresh token.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)

            if str(token['user_id']) != str(request.user.pk):
                raise PermissionDenied(
                    'El token no pertenece al usuario autenticado.'
                )

            token.blacklist()

            return Response(
                {'mensaje': 'Sesión cerrada correctamente.'},
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {'error': 'El token no es válido o ya fue utilizado.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class AdminUsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('id')
    serializer_class = AdminUsuarioSerializer
    permission_classes = [IsAuthenticated, SoloAdministrador]

    def perform_destroy(self, instance):
        if instance.pk == self.request.user.pk:
            raise PermissionDenied(
                'No podés eliminar tu propia cuenta de administrador.'
            )

        instance.delete()


