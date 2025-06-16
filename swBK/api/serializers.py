from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  PerfilUsuario, Empresa, TipoOportunidad, Oportunidad, Participacion, Notificacion, Provincia, Canton, Distrito, Event
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

#Serailizardor para el token
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
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

    def validateuser(self, attrs):
      
        username_or_email = attrs.get("username", None)  # Si no hay `username`, usa `email`
        password = attrs.get("password")

        if not username_or_email:
            raise serializers.ValidationError({"email": "Este campo es obligatorio."})

        user = authenticate(username=username_or_email, password=password)

        if user is None:
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                raise serializers.ValidationError("No active account found with the given credentials")

        if user:
            data = super().validate(attrs)
            data["role"] = user.groups.first().name if user.groups.exists() else "usuario"
            return data
        else:
            raise serializers.ValidationError("No active account found with the given credentials")
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
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
    def create(self, validated_data):
        usuario = User(
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
        
class EventSerializer(serializers.ModelSerializer):
    created_by = EmpresaSerializer()  # Incluye los datos de la empresa creadora

    class Meta:
        model = Event
        fields = [
             "title", "description", "date", "time", "location",
             "created_at", "created_by"
        ]
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
