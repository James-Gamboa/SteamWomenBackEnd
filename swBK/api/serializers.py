from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  PerfilUsuario, Empresa, TipoOportunidad, Oportunidad, Participacion, Notificacion, Provincia, Canton, Distrito
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Obtener el primer grupo del usuario (asumiendo 1 grupo por usuario)
        group = user.groups.first()
        token['role'] = group.name if group else None

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['role'] = refresh.payload.get('role')
        
        return data

# Serializador para Provincias
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'

# Serializador para Cantones
class CantonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canton
        fields = '__all__'

# Serializador para Distritos
class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        fields = '__all__'

# Serializador para el modelo User de Django
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)  # Validación de contraseña
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', "password"]
    def create(self, validated_data):
        usuario = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        usuario.set_password(validated_data["password"])  # Encriptación de contraseña
        usuario.save()
        return usuario

# Serializador para PerfilUsuario (información adicional vinculada a User)
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Incluye la información del usuario

    class Meta:
        model = PerfilUsuario
        fields = ['user', 'descripcion', 'cv_url', 'linkedin_url', 'provincia', 'canton', 'distrito']

# Serializador para Empresas
class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

# Serializador para Tipos de Oportunidad
class TipoOportunidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoOportunidad
        fields = '__all__'

# Serializador para Oportunidades
class OportunidadSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    tipo_oportunidad = TipoOportunidadSerializer()

    class Meta:
        model = Oportunidad
        fields = '__all__'

# Serializador para Participaciones
class ParticipacionSerializer(serializers.ModelSerializer):
    usuario = User()
    oportunidad = OportunidadSerializer()

    class Meta:
        model = Participacion
        fields = '__all__'

# Serializador para Notificaciones
class NotificacionSerializer(serializers.ModelSerializer):
    usuario = User()
    oportunidad = OportunidadSerializer()

    class Meta:
        model = Notificacion
        fields = '__all__'
