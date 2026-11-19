

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


Usuario = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        usuario = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            rol=Usuario.Rol.USUARIO
        )

        return usuario


class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'rol'
        ]
        read_only_fields = [
            'id',
            'username',
            'rol'
        ]


