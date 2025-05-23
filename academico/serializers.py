from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from djoser.serializers import UserSerializer
from .models import Usuario, Coordinador, User, Sede, Evaluacion, Calificacion, Rector
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
    username     = serializers.CharField(source='user.username')
    email        = serializers.EmailField(source='user.email')
    password     = serializers.CharField(write_only=True, source='user.password')
    first_name   = serializers.CharField(source='user.first_name')
    last_name    = serializers.CharField(source='user.last_name')

    # Campos personalizados de Usuario
    tipo_usr = serializers.ChoiceField(choices=Usuario.TIPO_USUARIO)

    # Comunes
    documento = serializers.CharField(required=False)
    tipo_documento = serializers.CharField(required=False)
    fecha_nacimiento = serializers.DateField(required=False)
    telefono = serializers.CharField(required=False)
    direccion = serializers.CharField(required=False)
    nombres = serializers.CharField(required=False)
    apellidos = serializers.CharField(required=False)
    

    # Específicos por tipo
    sexo = serializers.CharField(required=False)  
    estado = serializers.CharField(required=False) 
    grupo = serializers.UUIDField(required=False)
    sede = serializers.CharField(required=False)

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'tipo_usr', 'documento', 'tipo_documento', 'fecha_nacimiento',
            'telefono', 'direccion', 'sexo', 'estado', 'nombres',
            'apellidos', 'grupo', 'sede'
        ]

    def validate(self, attrs):
        tipo = attrs.get('tipo_usr')
        missing = []

        if tipo in ['estudiante', 'docente', 'coordinador', 'rector']:
            for field in ['documento', 'tipo_documento', 'fecha_nacimiento', 'telefono', 'direccion']:
                if not attrs.get(field):
                    missing.append(field)

        if tipo in ['coordinador', 'rector'] and not attrs.get('sexo'):
            missing.append('sexo')

        if tipo in ['estudiante', 'docente' , 'rector', 'coordinador'] and not attrs.get('estado'):
            missing.append('estado')

        if missing:
            raise ValidationError({field: 'Este campo es obligatorio para el tipo seleccionado.' for field in missing})

        # Validación del campo estado
        estado = attrs.get('estado')
        if tipo == 'rector' and estado and estado not in ['activo', 'inactivo']:
            raise ValidationError({'estado': 'Estado inválido para rector.'})
        if tipo == 'coordinador' and estado and estado not in ['activo', 'inactivo']:
            raise ValidationError({'estado': 'Estado inválido para coordinador.'})
        if tipo == 'docente' and estado and estado not in ['activo', 'inactivo']:
            raise ValidationError({'estado': 'Estado inválido para docente.'})
        if tipo == 'estudiante' and estado and estado not in ['activo', 'graduado', 'inactivo']:
            raise ValidationError({'estado': 'Estado inválido para estudiante.'})

        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop('user')  # ← Aquí vienen username, email, etc.
        password = user_data.pop('password')
        tipo = validated_data.pop('tipo_usr')

        # Datos comunes
        documento = validated_data.pop('documento', None)
        tipo_documento = validated_data.pop('tipo_documento', None)
        fecha_nacimiento = validated_data.pop('fecha_nacimiento', None)
        telefono = validated_data.pop('telefono', None)
        direccion = validated_data.pop('direccion', None)
        nombres = validated_data.pop('nombres', user_data.get('first_name', ''))
        apellidos = validated_data.pop('apellidos', user_data.get('last_name', ''))


        # Datos específicos
        sexo = validated_data.pop('sexo', None)
        estado = validated_data.pop('estado', None)
        grupo = validated_data.pop('grupo', None) 
        sede_codigo = validated_data.pop('sede', None)
        
        
        if tipo == 'estudiante':
         if not grupo:
            raise serializers.ValidationError({"grupo": "Este campo es requerido para estudiantes."})
         try:
            grupo = Grupo.objects.get(id=grupo)
         except Grupo.DoesNotExist:
            raise serializers.ValidationError({"grupo": "Grupo no encontrado."})
        
        
        if tipo == 'rector':
            try:
                sede = Sede.objects.get(codigo_dane=sede_codigo)
            except Sede.DoesNotExist:
                raise serializers.ValidationError({'sede_id': 'Sede no encontrada.'})



        try:
            user = User.objects.create_user(
                password=password,
                **user_data  # contiene username, email, first_name, last_name
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

        if tipo == 'estudiante':
            perfil_args['estado'] = estado
            Estudiante.objects.create( usuario=usuario,
            nombres=nombres,
            apellidos=apellidos,
            correo=user.email,
            tipo_documento=tipo_documento,
            numero_documento=documento,
            telefono=telefono,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            estado=estado,
            grupo=grupo
            )
        elif tipo == 'docente':
            perfil_args['estado'] = estado
            Docente.objects.create(
            usuario=usuario,
            nombres=nombres,
            apellidos=apellidos,
            tipo_documento=tipo_documento,
            numero_documento=documento,
            correo=user.email,
            telefono=telefono,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            estado=estado,
            )
        elif tipo == 'coordinador':
            perfil_args['sexo'] = sexo
            Coordinador.objects.create(
            usuario=usuario,
            tipo_documento=tipo_documento,
            numero_documento=documento,
            nombres=nombres,
            apellidos=apellidos,
            sexo=sexo,
            telefono=telefono,
            correo=user.email,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            estado=estado,
            )
        elif tipo == 'rector':
            perfil_args['sexo'] = sexo
            Rector.objects.create(
            usuario=usuario,
            tipo_documento=tipo_documento,
            numero_documento=documento,
            nombres=nombres,
            apellidos=apellidos,
            sexo=sexo,
            telefono=telefono,
            correo=user.email,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            sede_id=sede.codigo_dane,
            estado=estado,
            )

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
    estudiante = EstudianteSerializer(read_only=True)
    grupo = GrupoSerializer(read_only=True)
    asignatura = AsignaturaSerializer(read_only=True)

    class Meta:
        model = EstudianteAsignaturaCursoGrado
        fields = ['id', 'estudiante', 'grupo', 'grado', 'asignatura']

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
    
    def get(self, request, grupo_id):
        estudiantes = Estudiante.objects.filter(grupo_id=grupo_id)
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)
      
class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['codigo_dane', 'nombre']           

class RectorPerfilSerializer(serializers.ModelSerializer):
    tipo_usr = serializers.CharField(source='usuario.tipo_usr')
    username = serializers.CharField(source='usuario.user.username')
    email = serializers.EmailField(source='correo')

    class Meta:
        model = Rector
        fields = [
            'username',
            'tipo_usr',
            'nombres',
            'apellidos',
            'email',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'sexo'
        ]

class EstudiantePerfilSerializer(serializers.ModelSerializer):
    tipo_usr = serializers.CharField(source='usuario.tipo_usr')
    username = serializers.CharField(source='usuario.user.username')
    email = serializers.EmailField(source='correo')

    class Meta:
        model = Estudiante
        fields = [
            'username',
            'tipo_usr',
            'nombres',
            'apellidos',
            'email',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'sexo',
            'estado',
        ]

class DocentePerfilSerializer(serializers.ModelSerializer):
    tipo_usr = serializers.CharField(source='usuario.tipo_usr')
    username = serializers.CharField(source='usuario.user.username')
    email = serializers.EmailField(source='correo')

    class Meta:
        model = Docente
        fields = [
            'username',
            'tipo_usr',
            'nombres',
            'apellidos',
            'email',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'estado'
        ]

class CoordinadorPerfilSerializer(serializers.ModelSerializer):
    tipo_usr = serializers.CharField(source='usuario.tipo_usr')
    username = serializers.CharField(source='usuario.user.username')
    email = serializers.EmailField(source='correo')

    class Meta:
        model = Coordinador
        fields = [
            'username',
            'tipo_usr',
            'nombres',
            'apellidos',
            'email',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'sexo'
        ]       
        
class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = ['id', 'nombre', 'tipo', 'fecha', 'asignatura', 'grupo']
              
class CalificacionSerializer(serializers.ModelSerializer):
    nombre_estudiante = serializers.SerializerMethodField()

    class Meta:
        model = Calificacion
        fields = [
            'id',
            'evaluacion',
            'estudiante',
            'nombre_estudiante',
            'nota',
            'observaciones'
        ]

    def validate_nota(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("La nota debe estar entre 0 y 5")
        return value

    def get_nombre_estudiante(self, obj):
        return f"{obj.estudiante.nombres} {obj.estudiante.apellidos}"



class NotaFinalEstudianteSerializer(serializers.Serializer):
    estudiante = serializers.CharField()
    grupo = serializers.CharField()
    asignatura = serializers.CharField()
    actividades = serializers.ListField(child=serializers.FloatField())
    examenes_finales = serializers.ListField(child=serializers.FloatField())
    asistencia = serializers.FloatField()
    disciplina = serializers.FloatField()
    nota_final = serializers.FloatField()
    

class GrupoSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nombre']

class AsignaturaSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = ['id', 'nombre']

class AsignaturaDocenteGrupoExpandidoSerializer(serializers.ModelSerializer):
    asignatura = AsignaturaSerializerMini(read_only=True)
    grupo = GrupoSerializerMini(read_only=True)

    class Meta:
        model = AsignaturaDocenteGrupo
        fields = ['id', 'asignatura', 'grupo']
        
    