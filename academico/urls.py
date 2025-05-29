from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocenteViewSet, EstudianteViewSet, GradoViewSet, GrupoViewSet, AsignaturaViewSet, 
    AsignaturaDocenteGrupoViewSet, EstudianteAsignaturaCursoGradoViewSet, RegistroUsuarioView,
    SedeListView, PerfilDetalladoAPIView, EvaluacionesDocenteAPIView, CalificacionCreateAPIView,
    NotaFinalViewSet, AsignaturasGruposDocenteAPIView, PeriodoAcademicoActualView
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
router.register(r'sedes', SedeListView)
router.register(r'notas-finales', NotaFinalViewSet, basename='notas-finales')

urlpatterns = [
    path('', include(router.urls)),
    path('perfil-detallado/', PerfilDetalladoAPIView.as_view(), name='perfil-detallado'),
    path('docente/evaluaciones/', EvaluacionesDocenteAPIView.as_view(), name='evaluaciones-docente'),
    path('docente/calificaciones/', CalificacionCreateAPIView.as_view(), name='calificaciones-create'),
    path('docente/asignaturas-grupos/', AsignaturasGruposDocenteAPIView.as_view(), name='asignaturas-grupos-docente'),
    path('periodo-actual/', PeriodoAcademicoActualView.as_view(), name='periodo-actual'),

]

