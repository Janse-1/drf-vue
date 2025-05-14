from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer, ValidationError, IntegrityError
from .models import Usuario, Padre, Coordinador, User
from .models import Docente, Estudiante, Grado, Grupo, Asignatura, AsignaturaDocenteGrupo, EstudianteAsignaturaCursoGrado

#Aqui retorna datos GET
class UsuarioConTipoSerializer(serializers.ModelSerializer):
    tipo_usr = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'tipo_usr')

    def get_tipo_usr(self, obj):
        return obj.usuario.tipo_usr if hasattr(obj, 'usuario') else None



#Aquí para registrar usuarios POST
class UsuarioRegistroSerializer(serializers.ModelSerializer):
# Campos del modelo User
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    # Campos personalizados de Usuario
    tipo_usr = serializers.ChoiceField(choices=Usuario.TIPO_USUARIO)

    # Comunes
    documento = serializers.CharField(required=False)
    tipo_documento = serializers.CharField(required=False)
    fecha_nacimiento = serializers.DateField(required=False)
    telefono = serializers.CharField(required=False)
    direccion = serializers.CharField(required=False)

    # Específicos por tipo
    sexo = serializers.CharField(required=False)  # Solo para coordinador
    estado = serializers.CharField(required=False)  # Para estudiante y docente

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'tipo_usr', 'documento', 'tipo_documento', 'fecha_nacimiento',
            'telefono', 'direccion', 'sexo', 'estado'
        ]

    def validate(self, attrs):
        tipo = attrs.get('tipo_usr')
        requeridos = ['documento', 'tipo_documento', 'fecha_nacimiento', 'telefono', 'direccion']

        missing = [field for field in requeridos if not attrs.get(field)]
        if tipo == 'COORDINADOR' and not attrs.get('sexo'):
            missing.append('sexo')
        if tipo in ['ESTUDIANTE', 'DOCENTE'] and not attrs.get('estado'):
            missing.append('estado')

        if missing:
            raise ValidationError({field: 'Este campo es obligatorio para el tipo seleccionado.' for field in missing})

        # Validación del campo estado
        estado = attrs.get('estado')
        if tipo == 'DOCENTE' and estado and estado not in ['ACTIVO', 'INACTIVO']:
            raise ValidationError({'estado': 'Estado inválido para docente.'})
        if tipo == 'ESTUDIANTE' and estado and estado not in ['ACTIVO', 'GRADUADO', 'INACTIVO']:
            raise ValidationError({'estado': 'Estado inválido para estudiante.'})

        return attrs

    def create(self, validated_data):
        tipo = validated_data.pop('tipo_usr')

        # Datos comunes
        documento = validated_data.pop('documento')
        tipo_documento = validated_data.pop('tipo_documento')
        fecha_nacimiento = validated_data.pop('fecha_nacimiento')
        telefono = validated_data.pop('telefono')
        direccion = validated_data.pop('direccion')

        # Datos User
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        # Datos específicos
        sexo = validated_data.pop('sexo', '')
        estado = validated_data.pop('estado', '')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        except IntegrityError:
            raise ValidationError({'username': 'Este nombre de usuario ya está en uso.'})

        usuario = Usuario.objects.create(user=user, tipo_usr=tipo)

        perfil_args = {
            'usuario': usuario,
            'documento': documento,
            'tipo_documento': tipo_documento,
            'fecha_nacimiento': fecha_nacimiento,
            'telefono': telefono,
            'direccion': direccion,
        }

        if tipo == 'ESTUDIANTE':
            perfil_args['estado'] = estado
            Estudiante.objects.create(**perfil_args)
        elif tipo == 'DOCENTE':
            perfil_args['estado'] = estado
            Docente.objects.create(**perfil_args)
        elif tipo == 'COORDINADOR':
            perfil_args['sexo'] = sexo
            Coordinador.objects.create(**perfil_args)
        elif tipo == 'PADRE':
            Padre.objects.create(**perfil_args)

        return usuario



class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'

    def validate_director_grupo(self, value):
        if Grupo.objects.filter(director_grupo=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Este docente ya es director de otro grupo.")
        return value

    def validate(self, data):
        if self.instance and self.instance.director_grupo and data.get("director_grupo") != self.instance.director_grupo:
            raise serializers.ValidationError("Este grupo ya tiene un director asignado.")
        return data


class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = '__all__'
        
        

class AsignaturaDocenteGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignaturaDocenteGrupo
        fields = '__all__'

    def validate(self, data):
        grupo = data.get('id_grupo')
        asignatura = data.get('id_asignatura')
        docente = data.get('id_docente')

        if AsignaturaDocenteGrupo.objects.filter(id_grupo=grupo, id_asignatura=asignatura).exists():
            raise serializers.ValidationError("Esta asignatura ya está asignada a este grupo.")
        
        if AsignaturaDocenteGrupo.objects.filter(
            id_asignatura=asignatura,
            id_docente=docente,
            id_grupo=grupo
        ).exists():
            raise serializers.ValidationError(
                "Este docente ya tiene asignada esta asignatura para este grupo."
            )
            
        return data


class EstudianteAsignaturaCursoGradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstudianteAsignaturaCursoGrado
        fields = '__all__'

    def validate(self, data):
        estudiante = data.get('estudiante')
        asignatura = data.get('asignatura')
        grupo = data.get('grupo')
        grado = data.get('grado')
        
        if grupo.grado != grado:
            raise serializers.ValidationError("El grupo asignado no pertenece al grado seleccionado.")

        if EstudianteAsignaturaCursoGrado.objects.filter(
            estudiante=estudiante,
            asignatura=asignatura,
            grupo=grupo,
            grado=grado
        ).exists():
            raise serializers.ValidationError(
                "Este estudiante ya tiene asignada esta asignatura para el mismo grupo y grado."
            )
        return data
    
    

