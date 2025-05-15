from rest_framework import viewsets, mixins
from .models import Docente, Estudiante, Grado, Grupo, Asignatura, AsignaturaDocenteGrupo, EstudianteAsignaturaCursoGrado, Usuario, Sede
from .serializers import DocenteSerializer, EstudianteSerializer, GradoSerializer, GrupoSerializer, AsignaturaSerializer, AsignaturaDocenteGrupoSerializer, EstudianteAsignaturaCursoGradoSerializer, UsuarioRegistroSerializer, SedeSerializer


class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

class GradoViewSet(viewsets.ModelViewSet):
    queryset = Grado.objects.all()
    serializer_class = GradoSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer

class AsignaturaDocenteGrupoViewSet(viewsets.ModelViewSet):
    queryset = AsignaturaDocenteGrupo.objects.all()
    serializer_class = AsignaturaDocenteGrupoSerializer
    
class EstudianteAsignaturaCursoGradoViewSet(viewsets.ModelViewSet):
    queryset = EstudianteAsignaturaCursoGrado.objects.all()
    serializer_class = EstudianteAsignaturaCursoGradoSerializer
    
class RegistroUsuarioView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegistroSerializer
    
    
class SedeListView(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer