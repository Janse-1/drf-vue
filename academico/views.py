from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Docente, Estudiante, Grado, Grupo, Asignatura, Evaluacion, AsignaturaDocenteGrupo, EstudianteAsignaturaCursoGrado, Usuario, Sede, Coordinador, Padre, Calificacion
from .serializers import (DocenteSerializer, EstudianteSerializer, GradoSerializer, GrupoSerializer,
                          AsignaturaSerializer, AsignaturaDocenteGrupoSerializer, EstudianteAsignaturaCursoGradoSerializer,
                          UsuarioRegistroSerializer, SedeSerializer, EstudiantePerfilSerializer, DocentePerfilSerializer,
                          CoordinadorPerfilSerializer, PadrePerfilSerializer, EvaluacionSerializer, CalificacionSerializer,
                          NotaFinalEstudianteSerializer, AsignaturaDocenteGrupoExpandidoSerializer
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['grupo', 'asignatura']
    
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
    
    
class EvaluacionesDocenteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        docente = getattr(user.usuario, 'docente', None)

        if not docente:
            return Response({'detail': 'No autorizado como docente'}, status=403)

        grupo_id = request.GET.get('grupo_id')
        asignatura_id = request.GET.get('asignatura_id')

        if grupo_id and asignatura_id:
            asignacion_valida = AsignaturaDocenteGrupo.objects.filter(
                docente=docente,
                grupo_id=grupo_id,
                asignatura_id=asignatura_id
            ).exists()

            if not asignacion_valida:
                return Response({'detail': 'No autorizado para esta asignación'}, status=403)

            evaluaciones = Evaluacion.objects.filter(
                grupo_id=grupo_id,
                asignatura_id=asignatura_id
            ).order_by('fecha')
        else:
            evaluaciones = Evaluacion.objects.filter(
                asignatura__asignaturadocentegrupo__docente=docente
            ).distinct().order_by('fecha')

        serializer = EvaluacionSerializer(evaluaciones, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("Entró al metodo post")
        user = request.user
        docente = getattr(user.usuario, 'docente', None)

        if not docente:
            return Response({'detail': 'No autorizado como docente'}, status=403)

        data = request.data
        grupo_id = data.get('grupo')
        asignatura_id = data.get('asignatura')

        # Validar asignación docente
        asignacion_valida = AsignaturaDocenteGrupo.objects.filter(
            docente=docente,
            grupo_id=grupo_id,
            asignatura_id=asignatura_id
        ).exists()

        if not asignacion_valida:
            return Response({'detail': 'No autorizado para esta asignación'}, status=403)

        serializer = EvaluacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        

class CalificacionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        docente = getattr(request.user.usuario, 'docente', None)
        if not docente:
            return Response({'detail': 'No autorizado como docente'}, status=403)

        data = request.data
        evaluacion_id = data.get('evaluacion')
        estudiante_id = data.get('estudiante')

        # Validar que exista la evaluación
        try:
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)
        except Evaluacion.DoesNotExist:
            return Response({'detail': 'Evaluación no encontrada'}, status=404)

        # Validar que el docente tiene esa asignación
        tiene_permiso = AsignaturaDocenteGrupo.objects.filter(
            docente=docente,
            grupo=evaluacion.grupo,
            asignatura=evaluacion.asignatura
        ).exists()

        if not tiene_permiso:
            return Response({'detail': 'No autorizado para evaluar este grupo/asignatura'}, status=403)

        # Validar que el estudiante pertenece a ese grupo
        try:
            estudiante = Estudiante.objects.get(id=estudiante_id)
            if estudiante.grupo != evaluacion.grupo:
                return Response({'detail': 'El estudiante no pertenece a este grupo'}, status=400)
        except Estudiante.DoesNotExist:
            return Response({'detail': 'Estudiante no encontrado'}, status=404)

        # Crear o actualizar calificación
        calificacion, created = Calificacion.objects.update_or_create(
            evaluacion=evaluacion,
            estudiante=estudiante,
            defaults={
                'nota': data.get('nota'),
                'observaciones': data.get('observaciones', '')
            }
        )

        serializer = CalificacionSerializer(calificacion)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    
    def get(self, request):
        docente = getattr(request.user.usuario, 'docente', None)
        if not docente:
            return Response({'detail': 'No autorizado como docente'}, status=403)

        evaluacion_id = request.GET.get('evaluacion')
        if not evaluacion_id:
            return Response({'detail': 'Se requiere el ID de la evaluación'}, status=400)

        try:
            evaluacion = Evaluacion.objects.get(id=evaluacion_id)
        except Evaluacion.DoesNotExist:
            return Response({'detail': 'Evaluación no encontrada'}, status=404)

        # Validar que sea una evaluación del docente
        es_del_docente = AsignaturaDocenteGrupo.objects.filter(
            docente=docente,
            grupo=evaluacion.grupo,
            asignatura=evaluacion.asignatura
        ).exists()

        if not es_del_docente:
            return Response({'detail': 'No autorizado para esta evaluación'}, status=403)

        calificaciones = Calificacion.objects.select_related('estudiante').filter(evaluacion=evaluacion)
        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data)
    
    
class NotaFinalEstudianteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        estudiante_id = request.query_params.get('estudiante')
        asignatura_id = request.query_params.get('asignatura')
        grupo_id = request.query_params.get('grupo')

        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        grupo = get_object_or_404(Grupo, id=grupo_id)
        asignatura = get_object_or_404(Asignatura, id=asignatura_id)

        if estudiante.grupo.id != grupo.id:
            return Response({'detail': 'El estudiante no pertenece al grupo indicado.'}, status=400)

        # Obtener evaluaciones de esta asignatura en el grupo
        evaluaciones = Evaluacion.objects.filter(grupo=grupo, asignatura=asignatura)

        actividades = []
        examenes = []
        asistencia = 0
        disciplina = 0

        for evaluacion in evaluaciones:
            calificacion = Calificacion.objects.filter(evaluacion=evaluacion, estudiante=estudiante).first()
            if not calificacion:
                continue

            if evaluacion.tipo == 'actividad':
                actividades.append(calificacion.nota)
            elif evaluacion.tipo == 'examen_final':
                examenes.append(calificacion.nota)
            elif evaluacion.tipo == 'asistencia':
                asistencia = calificacion.nota
            elif evaluacion.tipo == 'disciplina':
                disciplina = calificacion.nota

        def promedio(lista):
            return sum(lista) / len(lista) if lista else 0

        nota_actividad = promedio(actividades)
        nota_examen = promedio(examenes)
        nota_asistencia = asistencia
        nota_disciplina = disciplina

        nota_final = (
            Decimal(nota_actividad) * Decimal('0.6') +
            Decimal(nota_examen) * Decimal('0.2') +
            Decimal(nota_asistencia) * Decimal('0.1') +
            Decimal(nota_disciplina) * Decimal('0.1')
        )

        data = {
            'estudiante': f"{estudiante.nombres} {estudiante.apellidos}",
            'grupo': grupo.nombre,
            'asignatura': asignatura.nombre,
            'actividades': actividades,
            'examenes_finales': examenes,
            'asistencia': nota_asistencia,
            'disciplina': nota_disciplina,
            'nota_final': round(nota_final, 2)
        }

        serializer = NotaFinalEstudianteSerializer(data)
        return Response(serializer.data)


class AsignaturasGruposDocenteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docente = getattr(request.user.usuario, 'docente', None)
        if not docente:
            return Response({'detail': 'No autorizado como docente'}, status=403)

        asignaciones = AsignaturaDocenteGrupo.objects.filter(docente=docente).select_related('asignatura', 'grupo')
        serializer = AsignaturaDocenteGrupoExpandidoSerializer(asignaciones, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_info_docente(request):
    docente = request.user
    asignaciones = AsignaturaDocenteGrupo.objects.filter(docente__usuario=docente)
    grupos = Grupo.objects.filter(asignaturas__docente__usuario=docente).distinct()

    data = {
        'nombre': docente.get_full_name(),
        'asignatura': asignaciones[0].asignatura.nombre if asignaciones else '',
        'grupos': [{'id': g.id, 'nombre': g.nombre} for g in grupos]
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_info_docente(request):
    docente = request.user
    asignaciones = AsignaturaDocenteGrupo.objects.filter(docente__usuario=docente)
    grupos = Grupo.objects.filter(asignaturas__docente__usuario=docente).distinct()

    data = {
        'nombre': docente.get_full_name(),
        'asignatura': asignaciones[0].asignatura.nombre if asignaciones else '',
        'grupos': [{'id': g.id, 'nombre': g.nombre} for g in grupos]
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_estudiantes_grupo(request, grupo_id):
    estudiantes = Estudiante.objects.filter(grupo_id=grupo_id)
    data = [{'id': e.id, 'nombre': f'{e.usuario.first_name} {e.usuario.last_name}'} for e in estudiantes]
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_sede_coordinador(request):
    coordinador = request.user
    sede = get_object_or_404(Sede, coordinador__usuario=coordinador)

    grados = sede.grado_set.all()

    data = {
        'nombre': sede.nombre,
        'grados': [
            {
                'id': grado.id,
                'nombre': grado.nombre,
                'grupos': [
                    {
                        'id': grupo.id,
                        'nombre': grupo.nombre,
                        'estudiantes': [
                            {
                                'id': est.id,
                                'nombre': f'{est.usuario.first_name} {est.usuario.last_name}'
                            } for est in grupo.estudiante_set.all()
                        ]
                    } for grupo in grado.grupo_set.all()
                ]
            } for grado in grados
        ]
    }
    return Response(data)


