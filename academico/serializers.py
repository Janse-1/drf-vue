from rest_framework import serializers
from .models import Docente, Estudiante, Grado, Grupo, Asignatura, AsignaturaDocenteGrupo, EstudianteAsignaturaCursoGrado

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
    
    

