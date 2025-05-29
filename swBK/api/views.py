from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .permission import IsRol
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import (
    PerfilUsuario, Empresa, TipoOportunidad, Oportunidad, Participacion, 
    Notificacion, Provincia, Canton, Distrito
)
from .serializers import (
    ProvinciaSerializer, CantonSerializer, DistritoSerializer,
    UserSerializer, PerfilUsuarioSerializer, EmpresaSerializer,
    TipoOportunidadSerializer, OportunidadSerializer, 
    ParticipacionSerializer, NotificacionSerializer, CustomTokenObtainPairSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
# ---------------------------
# VISTAS PARA UBICACIONES
# ---------------------------

class ProvinciaListCreateAPIView(ListCreateAPIView):
    queryset = Provincia.objects.all()
    required_roles = ["admin"] 
    permission_classes = [IsRol]
    serializer_class = ProvinciaSerializer


class ProvinciaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Provincia.objects.all()
    required_roles = ["admin"] 
    permission_classes = [IsRol]
    serializer_class = ProvinciaSerializer



class CantonListCreateAPIView(ListCreateAPIView):
    queryset = Canton.objects.all()
    serializer_class = CantonSerializer
    permission_classes = [AllowAny]

class CantonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Canton.objects.all()
    serializer_class = CantonSerializer
    permission_classes = [AllowAny]


class DistritoListCreateAPIView(ListCreateAPIView):
    queryset = Distrito.objects.all()
    serializer_class = DistritoSerializer
    permission_classes = [AllowAny]

class DistritoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Distrito.objects.all()
    serializer_class = DistritoSerializer
    permission_classes = [AllowAny]


# ---------------------------
# VISTAS PARA USUARIOS Y PERFIL
# ---------------------------
# Aunque el modelo User viene de Django, si deseas exponer algún endpoint, puedes hacerlo:

class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permitir acceso a usuarios no autenticados

class UserDetailView(RetrieveUpdateDestroyAPIView):
    required_roles = ["admin"] 
    permission_classes = [IsRol]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request):
        return Response({"message": "Solo administradores pueden ver esto"})


# Para el perfil extendido mediante PerfilUsuario, filtramos por el usuario autenticado

class PerfilUsuarioListCreateAPIView(ListCreateAPIView):
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated, IsRol]
    required_roles = ["admin"] 

    def get_queryset(self):
        # Solo se regresará el perfil del usuario autenticado.
        return PerfilUsuario.objects.filter(user=self.request.user)

class PerfilUsuarioRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PerfilUsuario.objects.filter(user=self.request.user)


# ---------------------------
# VISTAS PARA EMPRESAS
# ---------------------------

class EmpresaListCreateAPIView(ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [AllowAny]

class EmpresaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [AllowAny]


# ---------------------------
# VISTAS PARA TIPOS DE OPORTUNIDAD
# ---------------------------

class TipoOportunidadListCreateAPIView(ListCreateAPIView):
    queryset = TipoOportunidad.objects.all()
    serializer_class = TipoOportunidadSerializer
    permission_classes = [AllowAny]

class TipoOportunidadRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TipoOportunidad.objects.all()
    serializer_class = TipoOportunidadSerializer
    permission_classes = [AllowAny]


# ---------------------------
# VISTAS PARA OPORTUNIDADES
# ---------------------------

class OportunidadListCreateAPIView(ListCreateAPIView):
    queryset = Oportunidad.objects.all()
    serializer_class = OportunidadSerializer
    required_roles = ["admin, user"] 
    permission_classes = [IsRol]

class OportunidadRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Oportunidad.objects.all()
    serializer_class = OportunidadSerializer
    required_roles = ["admin"] 
    permission_classes = [IsRol]


# ---------------------------
# VISTAS PARA PARTICIPACIONES
# ---------------------------
# Se filtra para que cada usuaria solo vea sus participaciones.

class ParticipacionListCreateAPIView(ListCreateAPIView):
    serializer_class = ParticipacionSerializer
    permission_classes = [IsAuthenticated, IsRol]
    required_roles = ["admin", "user"] 

    def get_queryset(self):
        return Participacion.objects.filter(usuario=self.request.user)

class ParticipacionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParticipacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Participacion.objects.filter(usuario=self.request.user)


# ---------------------------
# VISTAS PARA NOTIFICACIONES
# ---------------------------
# Al igual que las participaciones, se muestra solo la información para la usuaria autenticada.

class NotificacionListCreateAPIView(ListCreateAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)

class NotificacionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)
