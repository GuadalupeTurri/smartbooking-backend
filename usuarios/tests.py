
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

Usuario = get_user_model()


class UsuarioAPITests(APITestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='usuario_prueba',
            email='usuario@gmail.com',
            password='Prueba123!'
        )

        self.administrador = Usuario.objects.create_superuser(
            username='admin_prueba',
            email='admin@gmail.com',
            password='Admin123!'
        )

    def test_registro_usuario_correcto(self):
        respuesta = self.client.post(
            '/api/usuarios/registro/',
            {
                'username': 'nuevo_usuario',
                'email': 'nuevo@gmail.com',
                'password': 'NuevaPrueba123!'
            },
            format='json'
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Usuario.objects.filter(username='nuevo_usuario').exists()
        )

    def test_usuario_comun_no_puede_listar_usuarios(self):
        self.client.force_authenticate(user=self.usuario)

        respuesta = self.client.get('/api/usuarios/admin/usuarios/')

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_administrador_puede_listar_usuarios(self):
        self.client.force_authenticate(user=self.administrador)

        respuesta = self.client.get('/api/usuarios/admin/usuarios/')

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK
        )

    def test_usuario_no_autenticado_no_puede_ver_perfil(self):
        respuesta = self.client.get('/api/usuarios/perfil/')

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
