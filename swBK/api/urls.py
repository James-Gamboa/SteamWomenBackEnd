from django.urls import path
from .views import (
    ProvinciaListCreateAPIView, ProvinciaRetrieveUpdateDestroyAPIView,
    CantonListCreateAPIView, CantonRetrieveUpdateDestroyAPIView,
    DistritoListCreateAPIView, DistritoRetrieveUpdateDestroyAPIView,
    PerfilUsuarioListCreateAPIView, PerfilUsuarioRetrieveUpdateDestroyAPIView,
    EmpresaListCreateAPIView, EmpresaRetrieveUpdateDestroyAPIView,
    TipoOportunidadListCreateAPIView, TipoOportunidadRetrieveUpdateDestroyAPIView,
    OportunidadListCreateAPIView, OportunidadRetrieveUpdateDestroyAPIView,
    ParticipacionListCreateAPIView, ParticipacionRetrieveUpdateDestroyAPIView,
    NotificacionListCreateAPIView, NotificacionRetrieveUpdateDestroyAPIView, UserListCreateView, 
    UserDetailView, CustomTokenObtainPairView, EventListCreateAPIView, EventRetrieveUpdateDestroyAPIView
    
)

urlpatterns = [
    # Provincias
    path('provincias/', ProvinciaListCreateAPIView.as_view(), name='provincias-list'),
    path('provincias/<int:pk>/', ProvinciaRetrieveUpdateDestroyAPIView.as_view(), name='provincias-detail'),

    # Cantones
    path('cantones/', CantonListCreateAPIView.as_view(), name='cantones-list'),
    path('cantones/<int:pk>/', CantonRetrieveUpdateDestroyAPIView.as_view(), name='cantones-detail'),

    # Distritos
    path('distritos/', DistritoListCreateAPIView.as_view(), name='distritos-list'),
    path('distritos/<int:pk>/', DistritoRetrieveUpdateDestroyAPIView.as_view(), name='distritos-detail'),

    # Usuarios


    # Perfil de Usuario (extendido con PerfilUsuario)
    path('perfil/', PerfilUsuarioListCreateAPIView.as_view(), name='perfil-list'),
    path('perfil/<int:pk>/', PerfilUsuarioRetrieveUpdateDestroyAPIView.as_view(), name='perfil-detail'),

    # Empresas
    path('empresas/', EmpresaListCreateAPIView.as_view(), name='empresas-list'),
    path('empresas/<int:pk>/', EmpresaRetrieveUpdateDestroyAPIView.as_view(), name='empresas-detail'),

    # Tipos de Oportunidad
    path('tipos-oportunidad/', TipoOportunidadListCreateAPIView.as_view(), name='tipos-oportunidad-list'),
    path('tipos-oportunidad/<int:pk>/', TipoOportunidadRetrieveUpdateDestroyAPIView.as_view(), name='tipos-oportunidad-detail'),

    # Oportunidades
    path('oportunidades/', OportunidadListCreateAPIView.as_view(), name='oportunidades-list'),
    path('oportunidades/<int:pk>/', OportunidadRetrieveUpdateDestroyAPIView.as_view(), name='oportunidades-detail'),
    
    #Eventos
    path('eventos/', EventListCreateAPIView.as_view(), name='eventos-list'),
    path('eventos/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='eventos-detail'),

    # Participaciones
    path('participaciones/', ParticipacionListCreateAPIView.as_view(), name='participaciones-list'),
    path('participaciones/<int:pk>/', ParticipacionRetrieveUpdateDestroyAPIView.as_view(), name='participaciones-detail'),

    # Notificaciones
    path('notificaciones/', NotificacionListCreateAPIView.as_view(), name='notificaciones-list'),
    path('notificaciones/<int:pk>/', NotificacionRetrieveUpdateDestroyAPIView.as_view(), name='notificaciones-detail'),
    
    path('usuarios/', UserListCreateView.as_view(), name='usuario-listar-crear'),  # Para registrar usuarios
    path('usuarios/<int:pk>/', UserDetailView.as_view(), name='usuario-editar-actualizar'),  # Para ver/editar un usuario específico
    
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
    