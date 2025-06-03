import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from api.models import (
    User, PerfilUsuario, Empresa, Oportunidad, Evento,
    Requisito, Beneficio, AgendaItem, Participacion,
    Provincia, Canton, Distrito, TipoOportunidad
)
from django.contrib.auth.models import Group

class ProvinciaType(DjangoObjectType):
    class Meta:
        model = Provincia
        fields = '__all__'

class CantonType(DjangoObjectType):
    class Meta:
        model = Canton
        fields = '__all__'

class DistritoType(DjangoObjectType):
    class Meta:
        model = Distrito
        fields = '__all__'

class TipoOportunidadType(DjangoObjectType):
    class Meta:
        model = TipoOportunidad
        fields = '__all__'

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active')

class PerfilUsuarioType(DjangoObjectType):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'

class EmpresaType(DjangoObjectType):
    class Meta:
        model = Empresa
        fields = '__all__'

class RequisitoType(DjangoObjectType):
    class Meta:
        model = Requisito
        fields = '__all__'

class BeneficioType(DjangoObjectType):
    class Meta:
        model = Beneficio
        fields = '__all__'

class AgendaItemType(DjangoObjectType):
    class Meta:
        model = AgendaItem
        fields = '__all__'

class OportunidadType(DjangoObjectType):
    requisitos = graphene.List(RequisitoType)
    beneficios = graphene.List(BeneficioType)
    empresa = graphene.Field(EmpresaType)
    tipo_oportunidad = graphene.Field(TipoOportunidadType)
    provincia = graphene.Field(ProvinciaType)
    canton = graphene.Field(CantonType)
    distrito = graphene.Field(DistritoType)

    class Meta:
        model = Oportunidad
        fields = '__all__'

class EventoType(DjangoObjectType):
    requisitos = graphene.List(RequisitoType)
    beneficios = graphene.List(BeneficioType)
    agenda = graphene.List(AgendaItemType)
    empresa = graphene.Field(EmpresaType)
    provincia = graphene.Field(ProvinciaType)
    canton = graphene.Field(CantonType)
    distrito = graphene.Field(DistritoType)

    class Meta:
        model = Evento
        fields = '__all__'

class ParticipacionType(DjangoObjectType):
    class Meta:
        model = Participacion
        fields = '__all__'

class Query(graphene.ObjectType):
    # User queries
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID())
    
    # Profile queries
    perfiles = graphene.List(PerfilUsuarioType)
    perfil = graphene.Field(PerfilUsuarioType, id=graphene.ID())
    
    # Company queries
    empresas = graphene.List(EmpresaType)
    empresa = graphene.Field(EmpresaType, id=graphene.ID())
    
    # Location queries
    provincias = graphene.List(ProvinciaType)
    cantones = graphene.List(CantonType, provincia_id=graphene.ID())
    distritos = graphene.List(DistritoType, canton_id=graphene.ID())
    
    # Opportunity queries
    oportunidades = graphene.List(OportunidadType, 
        tipo_id=graphene.ID(),
        modalidad=graphene.String(),
        provincia_id=graphene.ID()
    )
    oportunidad = graphene.Field(OportunidadType, id=graphene.ID(), slug=graphene.String())
    
    # Event queries
    eventos = graphene.List(EventoType,
        modalidad=graphene.String(),
        provincia_id=graphene.ID(),
        fecha_desde=graphene.Date(),
        fecha_hasta=graphene.Date()
    )
    evento = graphene.Field(EventoType, id=graphene.ID(), slug=graphene.String())

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

    def resolve_perfiles(self, info):
        return PerfilUsuario.objects.all()

    def resolve_perfil(self, info, id):
        return PerfilUsuario.objects.get(pk=id)

    def resolve_empresas(self, info):
        return Empresa.objects.all()

    def resolve_empresa(self, info, id):
        return Empresa.objects.get(pk=id)

    def resolve_provincias(self, info):
        return Provincia.objects.all()

    def resolve_cantones(self, info, provincia_id=None):
        if provincia_id:
            return Canton.objects.filter(provincia_id=provincia_id)
        return Canton.objects.all()

    def resolve_distritos(self, info, canton_id=None):
        if canton_id:
            return Distrito.objects.filter(canton_id=canton_id)
        return Distrito.objects.all()

    def resolve_oportunidades(self, info, tipo_id=None, modalidad=None, provincia_id=None):
        queryset = Oportunidad.objects.all()
        if tipo_id:
            queryset = queryset.filter(tipo_oportunidad_id=tipo_id)
        if modalidad:
            queryset = queryset.filter(modalidad=modalidad)
        if provincia_id:
            queryset = queryset.filter(provincia_id=provincia_id)
        return queryset

    def resolve_oportunidad(self, info, id=None, slug=None):
        if id:
            return Oportunidad.objects.get(pk=id)
        if slug:
            return Oportunidad.objects.get(slug=slug)

    def resolve_eventos(self, info, modalidad=None, provincia_id=None, fecha_desde=None, fecha_hasta=None):
        queryset = Evento.objects.all()
        if modalidad:
            queryset = queryset.filter(modalidad=modalidad)
        if provincia_id:
            queryset = queryset.filter(provincia_id=provincia_id)
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
        return queryset

    def resolve_evento(self, info, id=None, slug=None):
        if id:
            return Evento.objects.get(pk=id)
        if slug:
            return Evento.objects.get(slug=slug)

class CreateOportunidad(graphene.Mutation):
    class Arguments:
        titulo = graphene.String(required=True)
        descripcion = graphene.String(required=True)
        descripcion_completa = graphene.String(required=True)
        tipo_oportunidad_id = graphene.ID(required=True)
        fecha_inicio = graphene.Date(required=True)
        fecha_fin = graphene.Date(required=True)
        modalidad = graphene.String(required=True)
        empresa_id = graphene.ID(required=True)
        imagen = graphene.String()
        proceso_aplicacion = graphene.String(required=True)
        sitio_web = graphene.String()
        provincia_id = graphene.ID()
        canton_id = graphene.ID()
        distrito_id = graphene.ID()
        requisitos = graphene.List(graphene.String)
        beneficios = graphene.List(graphene.String)

    oportunidad = graphene.Field(OportunidadType)

    def mutate(self, info, **kwargs):
        requisitos = kwargs.pop('requisitos', [])
        beneficios = kwargs.pop('beneficios', [])
        
        oportunidad = Oportunidad.objects.create(**kwargs)
        
        # Crear y asociar requisitos
        for req in requisitos:
            requisito = Requisito.objects.create(descripcion=req)
            oportunidad.requisitos.add(requisito)
            
        # Crear y asociar beneficios
        for ben in beneficios:
            beneficio = Beneficio.objects.create(descripcion=ben)
            oportunidad.beneficios.add(beneficio)
            
        return CreateOportunidad(oportunidad=oportunidad)

class UpdateOportunidad(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        titulo = graphene.String()
        descripcion = graphene.String()
        descripcion_completa = graphene.String()
        tipo_oportunidad_id = graphene.ID()
        fecha_inicio = graphene.Date()
        fecha_fin = graphene.Date()
        modalidad = graphene.String()
        empresa_id = graphene.ID()
        imagen = graphene.String()
        proceso_aplicacion = graphene.String()
        sitio_web = graphene.String()
        provincia_id = graphene.ID()
        canton_id = graphene.ID()
        distrito_id = graphene.ID()
        requisitos = graphene.List(graphene.String)
        beneficios = graphene.List(graphene.String)

    oportunidad = graphene.Field(OportunidadType)

    def mutate(self, info, id, **kwargs):
        oportunidad = Oportunidad.objects.get(pk=id)
        
        requisitos = kwargs.pop('requisitos', None)
        beneficios = kwargs.pop('beneficios', None)
        
        for key, value in kwargs.items():
            if value is not None:
                setattr(oportunidad, key, value)
        
        if requisitos is not None:
            oportunidad.requisitos.clear()
            for req in requisitos:
                requisito = Requisito.objects.create(descripcion=req)
                oportunidad.requisitos.add(requisito)
                
        if beneficios is not None:
            oportunidad.beneficios.clear()
            for ben in beneficios:
                beneficio = Beneficio.objects.create(descripcion=ben)
                oportunidad.beneficios.add(beneficio)
        
        oportunidad.save()
        return UpdateOportunidad(oportunidad=oportunidad)

class DeleteOportunidad(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            oportunidad = Oportunidad.objects.get(pk=id)
            oportunidad.delete()
            return DeleteOportunidad(success=True)
        except Oportunidad.DoesNotExist:
            return DeleteOportunidad(success=False)

class CreateEvento(graphene.Mutation):
    class Arguments:
        titulo = graphene.String(required=True)
        descripcion = graphene.String(required=True)
        descripcion_completa = graphene.String(required=True)
        fecha = graphene.Date(required=True)
        hora = graphene.Time(required=True)
        modalidad = graphene.String(required=True)
        empresa_id = graphene.ID(required=True)
        imagen = graphene.String()
        capacidad = graphene.Int(required=True)
        precio = graphene.Float(required=True)
        sitio_web = graphene.String()
        url_registro = graphene.String()
        provincia_id = graphene.ID()
        canton_id = graphene.ID()
        distrito_id = graphene.ID()
        requisitos = graphene.List(graphene.String)
        beneficios = graphene.List(graphene.String)
        agenda = graphene.List(graphene.JSONString)

    evento = graphene.Field(EventoType)

    def mutate(self, info, **kwargs):
        requisitos = kwargs.pop('requisitos', [])
        beneficios = kwargs.pop('beneficios', [])
        agenda_items = kwargs.pop('agenda', [])
        
        evento = Evento.objects.create(**kwargs)
        
        # Crear y asociar requisitos
        for req in requisitos:
            requisito = Requisito.objects.create(descripcion=req)
            evento.requisitos.add(requisito)
            
        # Crear y asociar beneficios
        for ben in beneficios:
            beneficio = Beneficio.objects.create(descripcion=ben)
            evento.beneficios.add(beneficio)
            
        # Crear y asociar items de agenda
        for item in agenda_items:
            agenda_item = AgendaItem.objects.create(
                hora=item.get('time'),
                actividad=item.get('activity'),
                descripcion=item.get('description')
            )
            evento.agenda.add(agenda_item)
            
        return CreateEvento(evento=evento)

class UpdateEvento(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        titulo = graphene.String()
        descripcion = graphene.String()
        descripcion_completa = graphene.String()
        fecha = graphene.Date()
        hora = graphene.Time()
        modalidad = graphene.String()
        empresa_id = graphene.ID()
        imagen = graphene.String()
        capacidad = graphene.Int()
        precio = graphene.Float()
        sitio_web = graphene.String()
        url_registro = graphene.String()
        provincia_id = graphene.ID()
        canton_id = graphene.ID()
        distrito_id = graphene.ID()
        requisitos = graphene.List(graphene.String)
        beneficios = graphene.List(graphene.String)
        agenda = graphene.List(graphene.JSONString)

    evento = graphene.Field(EventoType)

    def mutate(self, info, id, **kwargs):
        evento = Evento.objects.get(pk=id)
        
        requisitos = kwargs.pop('requisitos', None)
        beneficios = kwargs.pop('beneficios', None)
        agenda_items = kwargs.pop('agenda', None)
        
        for key, value in kwargs.items():
            if value is not None:
                setattr(evento, key, value)
        
        if requisitos is not None:
            evento.requisitos.clear()
            for req in requisitos:
                requisito = Requisito.objects.create(descripcion=req)
                evento.requisitos.add(requisito)
                
        if beneficios is not None:
            evento.beneficios.clear()
            for ben in beneficios:
                beneficio = Beneficio.objects.create(descripcion=ben)
                evento.beneficios.add(beneficio)
                
        if agenda_items is not None:
            evento.agenda.clear()
            for item in agenda_items:
                agenda_item = AgendaItem.objects.create(
                    hora=item.get('time'),
                    actividad=item.get('activity'),
                    descripcion=item.get('description')
                )
                evento.agenda.add(agenda_item)
        
        evento.save()
        return UpdateEvento(evento=evento)

class DeleteEvento(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            evento = Evento.objects.get(pk=id)
            evento.delete()
            return DeleteEvento(success=True)
        except Evento.DoesNotExist:
            return DeleteEvento(success=False)

class CreateEstudiante(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        descripcion = graphene.String()
        cv_url = graphene.String()
        linkedin_url = graphene.String()
        provincia_id = graphene.ID()
        canton_id = graphene.ID()
        distrito_id = graphene.ID()

    user = graphene.Field(UserType)
    perfil = graphene.Field(PerfilUsuarioType)

    def mutate(self, info, **kwargs):
        # Extraer datos del perfil
        perfil_data = {
            'descripcion': kwargs.pop('descripcion', ''),
            'cv_url': kwargs.pop('cv_url', ''),
            'linkedin_url': kwargs.pop('linkedin_url', ''),
            'provincia_id': kwargs.pop('provincia_id', None),
            'canton_id': kwargs.pop('canton_id', None),
            'distrito_id': kwargs.pop('distrito_id', None)
        }

        # Crear usuario
        user = User.objects.create_user(
            username=kwargs['username'],
            email=kwargs['email'],
            password=kwargs['password'],
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name']
        )

        # Asignar rol de estudiante
        grupo_estudiante, _ = Group.objects.get_or_create(name="estudiante")
        user.groups.add(grupo_estudiante)

        # Crear perfil
        perfil = PerfilUsuario.objects.create(
            user=user,
            **perfil_data
        )

        return CreateEstudiante(user=user, perfil=perfil)

class CreateEmpresa(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        nombre = graphene.String(required=True)
        descripcion = graphene.String(required=True)
        sitio_web = graphene.String()
        logo = graphene.String()
        provincia_id = graphene.ID()
        canton_id = graphene.ID()
        distrito_id = graphene.ID()

    user = graphene.Field(UserType)
    empresa = graphene.Field(EmpresaType)

    def mutate(self, info, **kwargs):
        # Extraer datos de la empresa
        empresa_data = {
            'nombre': kwargs.pop('nombre'),
            'descripcion': kwargs.pop('descripcion'),
            'sitio_web': kwargs.pop('sitio_web', ''),
            'logo': kwargs.pop('logo', ''),
            'provincia_id': kwargs.pop('provincia_id', None),
            'canton_id': kwargs.pop('canton_id', None),
            'distrito_id': kwargs.pop('distrito_id', None)
        }

        # Crear usuario
        user = User.objects.create_user(
            username=kwargs['username'],
            email=kwargs['email'],
            password=kwargs['password']
        )

        # Asignar rol de empresa
        grupo_empresa, _ = Group.objects.get_or_create(name="empresa")
        user.groups.add(grupo_empresa)

        # Crear empresa
        empresa = Empresa.objects.create(
            usuario=user,
            **empresa_data
        )

        return CreateEmpresa(user=user, empresa=empresa)

class Mutation(graphene.ObjectType):
    # JWT mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    # User registration mutations
    create_estudiante = CreateEstudiante.Field()
    create_empresa = CreateEmpresa.Field()

    # Custom mutations
    create_oportunidad = CreateOportunidad.Field()
    update_oportunidad = UpdateOportunidad.Field()
    delete_oportunidad = DeleteOportunidad.Field()
    create_evento = CreateEvento.Field()
    update_evento = UpdateEvento.Field()
    delete_evento = DeleteEvento.Field()

schema = graphene.Schema(query=Query, mutation=Mutation) 