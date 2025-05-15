from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Docente, Estudiante, Grado, Grupo, Asignatura, AsignaturaDocenteGrupo, EstudianteAsignaturaCursoGrado, Usuario, Sede, Coordinador, Padre
from .serializers import (DocenteSerializer, EstudianteSerializer, GradoSerializer, GrupoSerializer,
                          AsignaturaSerializer, AsignaturaDocenteGrupoSerializer, EstudianteAsignaturaCursoGradoSerializer,
                          UsuarioRegistroSerializer, SedeSerializer, EstudiantePerfilSerializer, DocentePerfilSerializer,
                          CoordinadorPerfilSerializer, PadrePerfilSerializer
                          )


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
    
    
    
class PerfilDetalladoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            usuario = user.usuario  
        except Usuario.DoesNotExist:
            return Response({"detail": "Usuario no tiene perfil asociado."}, status=400)

        tipo = usuario.tipo_usr

        if tipo == 'estudiante':
            try:
                perfil = Estudiante.objects.get(usuario=usuario)
                serializer = EstudiantePerfilSerializer(perfil)
            except Estudiante.DoesNotExist:
                return Response({"detail": "Perfil de estudiante no encontrado"}, status=404)

        elif tipo == 'docente':
            try:
                perfil = Docente.objects.get(usuario=usuario)
                serializer = DocentePerfilSerializer(perfil)
            except Docente.DoesNotExist:
                return Response({"detail": "Perfil de docente no encontrado"}, status=404)

        elif tipo == 'coordinador':
            try:
                perfil = Coordinador.objects.get(usuario=usuario)
                serializer = CoordinadorPerfilSerializer(perfil)
            except Coordinador.DoesNotExist:
                return Response({"detail": "Perfil de coordinador no encontrado"}, status=404)

        elif tipo == 'padre':
            try:
                perfil = Padre.objects.get(usuario=usuario)
                serializer = PadrePerfilSerializer(perfil)
            except Padre.DoesNotExist:
                return Response({"detail": "Perfil de padre no encontrado"}, status=404)

        else:
            return Response({"detail": "Tipo de usuario no válido"}, status=400)

        return Response(serializer.data)