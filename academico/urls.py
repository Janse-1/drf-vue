from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocenteViewSet, EstudianteViewSet, GradoViewSet, GrupoViewSet, AsignaturaViewSet, 
    AsignaturaDocenteGrupoViewSet, EstudianteAsignaturaCursoGradoViewSet, RegistroUsuarioView,
    SedeListView, PerfilDetalladoAPIView, EvaluacionesDocenteAPIView, CalificacionCreateAPIView,
    NotaFinalViewSet, AsignaturasGruposDocenteAPIView, PeriodoAcademicoActualView, SedeResumenAPIView,
    CoordinadoresDisponiblesAPIView, SedesDisponiblesAPIView, AsignarCoordinadorSedeAPIView, DetalleSedeAPIView,
    CoordinadorViewSet
)

router = DefaultRouter()
router.register(r'docentes', DocenteViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'grados', GradoViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'asignaturas', AsignaturaViewSet)
router.register(r'asignatura-docente-grupo', AsignaturaDocenteGrupoViewSet)
router.register(r'estudiante-asignatura-curso-grado', EstudianteAsignaturaCursoGradoViewSet)
router.register(r'registro', RegistroUsuarioView, basename='registro-usuario')
router.register(r'sedes', SedeListView, basename='sedes')
router.register(r'notas-finales', NotaFinalViewSet, basename='notas-finales')
router.register(r'coordinadores', CoordinadorViewSet, basename='coordinadores')

urlpatterns = [
    path('', include(router.urls)),
    path('perfil-detallado/', PerfilDetalladoAPIView.as_view(), name='perfil-detallado'),
    path('docente/evaluaciones/', EvaluacionesDocenteAPIView.as_view(), name='evaluaciones-docente'),
    path('docente/calificaciones/', CalificacionCreateAPIView.as_view(), name='calificaciones-create'),
    path('docente/asignaturas-grupos/', AsignaturasGruposDocenteAPIView.as_view(), name='asignaturas-grupos-docente'),
    path('periodo-actual/', PeriodoAcademicoActualView.as_view(), name='periodo-actual'),
    path('resumen-sedes/', SedeResumenAPIView.as_view(), name='sede-resumen'),
    path('coordinadores-disponibles/', CoordinadoresDisponiblesAPIView.as_view(), name='coordinadores-disponibles'),
    path('sedes-disponibles/', SedesDisponiblesAPIView.as_view(), name='sedes-disponibles'),
    path('asignar-coordinador-sede/', AsignarCoordinadorSedeAPIView.as_view(), name='asignar-coordinador-sede'),
    path('detalle-sede/<str:codigo_dane>/', DetalleSedeAPIView.as_view(), name='detalle-sede'),
]

