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

    # Campos personalizados de Usuario
    tipo_usr = serializers.ChoiceField(choices=Usuario.TIPO_USUARIO)

    # Datos específicos por tipo
    documento = serializers.CharField(required=False)
    telefono = serializers.CharField(required=False)
    direccion = serializers.CharField(required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'tipo_usr', 'documento', 'telefono', 'direccion']

    def create(self, validated_data):
        tipo = validated_data.pop('tipo_usr')
        documento = validated_data.pop('documento', '')
        telefono = validated_data.pop('telefono', '')
        direccion = validated_data.pop('direccion', '')
        
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        try:
        # Crear User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        except IntegrityError:
         raise ValidationError({'username': 'Este nombre de usuario ya está en uso.'})

        # Crear Usuario vinculado
        usuario = Usuario.objects.create(user=user, tipo_usr=tipo)

        # Crear el tipo específico
        if tipo == 'ESTUDIANTE':
            Estudiante.objects.create(usuario=usuario, documento=documento, telefono=telefono, direccion=direccion)
        elif tipo == 'DOCENTE':
            Docente.objects.create(usuario=usuario, documento=documento, telefono=telefono, direccion=direccion)
        elif tipo == 'PADRE':
            Padre.objects.create(usuario=usuario, documento=documento, telefono=telefono, direccion=direccion)
        elif tipo == 'COORDINADOR':
            Coordinador.objects.create(usuario=usuario, documento=documento, telefono=telefono, direccion=direccion)

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
    
    

