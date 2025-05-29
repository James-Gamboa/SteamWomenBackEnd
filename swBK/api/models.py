from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

from django.db import models

# Tabla de Provincias
class Provincia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Tabla de Cantones
class Canton(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Tabla de Distritos
class Distrito(models.Model):
    nombre = models.CharField(max_length=100)
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Tabla de Usuarios
class PerfilUsuario(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    descripcion = models.TextField(blank=True, null=True)  
    cv_url = models.URLField(blank=True, null=True)  
    linkedin_url = models.URLField(blank=True, null=True)  
    provincia = models.ForeignKey('Provincia', on_delete=models.SET_NULL, null=True)  
    canton = models.ForeignKey('Canton', on_delete=models.SET_NULL, null=True)  
    distrito = models.ForeignKey('Distrito', on_delete=models.SET_NULL, null=True)  

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Tabla de Empresas
class Empresa(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    email_contacto = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    sitio_web = models.URLField(blank=True, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    canton = models.ForeignKey(Canton, on_delete=models.SET_NULL, null=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre_empresa

# Tabla de Tipos de Oportunidad
class TipoOportunidad(models.Model):
    nombre_tipo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_tipo

# Tabla de Oportunidades
class Oportunidad(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo_oportunidad = models.ForeignKey(TipoOportunidad, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    modalidad = models.CharField(max_length=10, choices=[('Presencial', 'Presencial'), ('Virtual', 'Virtual')])
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True)
    canton = models.ForeignKey(Canton, on_delete=models.SET_NULL, null=True, blank=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.SET_NULL, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

# Tabla de Participaciones (Usuarios inscritos en oportunidades)
class Participacion(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    oportunidad = models.ForeignKey(Oportunidad, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
   

    def __str__(self):
        return f"{self.usuario} - {self.oportunidad}"

# Tabla de Notificaciones
class Notificacion(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    oportunidad = models.ForeignKey(Oportunidad, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=[('Leída', 'Leída'), ('No leída', 'No leída')])

    def __str__(self):
        return f"Notificación para {self.usuario}"
