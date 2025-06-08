from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from django.core.exceptions import MultipleObjectsReturned
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import (Docente, Estudiante, Grado, Grupo, Rector, Asignatura, Evaluacion, AsignaturaDocenteGrupo, 
                     EstudianteAsignaturaCursoGrado, Usuario, Sede, Coordinador, Calificacion, PeriodoAcademico,
                     NotaFinal, CoordinadorSede
                     )
from .serializers import (DocenteSerializer, EstudianteSerializer, GradoSerializer, GrupoSerializer,
                          AsignaturaSerializer, AsignaturaDocenteGrupoSerializer, EstudianteAsignaturaCursoGradoSerializer,
                          UsuarioRegistroSerializer, SedeSerializer, EstudiantePerfilSerializer, DocentePerfilSerializer,
                          CoordinadorPerfilSerializer,  EvaluacionSerializer, CalificacionSerializer,
                          NotaFinalSerializer, AsignaturaDocenteGrupoExpandidoSerializer, RectorPerfilSerializer,
                          PeriodoAcademicoSerializer, SedeResumenSerializer, CoordinadorSedeAsignarSerializer
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_grupo', 'id_docente', 'asignatura']

    @action(detail=False, methods=['get'], url_path='asignaturas-por-grupo')
    def asignaturas_por_grupo(self, request):
        grupo_id = request.query_params.get('grupo')
        if not grupo_id:
            return Response({"error": "Debe enviar el ID del grupo"}, status=400)
        
        relaciones = self.queryset.filter(grupo_id=grupo_id).select_related('asignatura')
        asignaturas = [rel.asignatura for rel in relaciones]
        data = AsignaturaSerializer(asignaturas, many=True).data
        return Response(data)
    
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()
     
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

        elif tipo == 'rector':
            try:
                perfil = Rector.objects.get(usuario=usuario)
                serializer = RectorPerfilSerializer(perfil)
            except Rector.DoesNotExist:
                return Response({"detail": "Perfil de rector no encontrado"}, status=404)

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
        
class NotaFinalViewSet(viewsets.ModelViewSet):
    queryset = NotaFinal.objects.all()
    serializer_class = NotaFinalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estudiante', 'grupo', 'asignatura', 'periodo']

    @action(detail=False, methods=['post'], url_path='bulk_create')
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Notas guardadas exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AsignaturasGruposDocenteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docente = getattr(request.user.usuario, 'docente', None)
        if not docente:
            return Response({'detail': 'No autorizado como docente'}, status=403)

        asignaciones = AsignaturaDocenteGrupo.objects.filter(docente=docente).select_related('asignatura', 'grupo')
        serializer = AsignaturaDocenteGrupoExpandidoSerializer(asignaciones, many=True, context={'request': request})

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


class PeriodoAcademicoActualView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        fecha_actual = now().date()
        try:
            periodo = PeriodoAcademico.objects.get(
                fecha_inicio__lte=fecha_actual,
                fecha_fin__gte=fecha_actual
            )
            serializer = PeriodoAcademicoSerializer(periodo)
            return Response(serializer.data)
        except PeriodoAcademico.DoesNotExist:
            return Response({"detail": "No hay un periodo académico activo."}, status=404)
        except MultipleObjectsReturned:
            return Response({"detail": "Hay más de un periodo activo. Corrige los datos."}, status=500)
        
        
class SedeResumenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sedes = Sede.objects.all()
        serializer = SedeResumenSerializer(sedes, many=True)
        return Response(serializer.data)


class CoordinadoresDisponiblesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        coordinadores = Coordinador.objects.exclude(coordinadorsede__isnull=False)
        data = [
            {
                'id': str(c.id),
                'nombres': c.nombres,
                'apellidos': c.apellidos
            } for c in coordinadores
        ]
        return Response(data)

class SedesDisponiblesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sedes = Sede.objects.exclude(coordinadorsede__isnull=False)
        data = [
            {
                'codigo_dane': s.codigo_dane,
                'nombre': s.nombre
            } for s in sedes
        ]
        return Response(data)

class AsignarCoordinadorSedeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CoordinadorSedeAsignarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Coordinador asignado correctamente.'}, status=status.HTTP_201_CREATED)

class DetalleSedeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, codigo_dane):
        try:
            sede = Sede.objects.get(codigo_dane=codigo_dane)
        except Sede.DoesNotExist:
            return Response({'detail': 'Sede no encontrada.'}, status=404)
        # Coordinador
        rel = CoordinadorSede.objects.filter(sede=sede).select_related('coordinador').first()
        coordinador = None
        if rel and rel.coordinador:
            coordinador = {
                'id': str(rel.coordinador.id),
                'nombre': f"{rel.coordinador.nombres} {rel.coordinador.apellidos}"
            }
        # Docentes
        docentes = Docente.objects.filter(docentesede__sede=sede).distinct()
        docentes_list = [
            {'id': str(d.id), 'nombres': d.nombres, 'apellidos': d.apellidos}
            for d in docentes
        ]
        # Grados
        grados = Grado.objects.filter(sede=sede)
        grados_list = [{'id': str(g.id), 'nombre': g.nombre} for g in grados]
        # Grupos
        grupos = Grupo.objects.filter(grado__sede=sede)
        grupos_list = [{'id': str(gr.id), 'nombre': gr.nombre} for gr in grupos]
        # Estudiantes
        estudiantes = Estudiante.objects.filter(grupo__grado__sede=sede)
        estudiantes_list = [
            {'id': str(e.id), 'nombres': e.nombres, 'apellidos': e.apellidos}
            for e in estudiantes
        ]
        return Response({
            'codigo_dane': sede.codigo_dane,
            'nombre': sede.nombre,
            'coordinador': coordinador,
            'docentes': docentes_list,
            'grados': grados_list,
            'grupos': grupos_list,
            'estudiantes': estudiantes_list
        })
