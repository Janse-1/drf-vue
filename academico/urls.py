from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocenteViewSet, EstudianteViewSet, GradoViewSet, GrupoViewSet, AsignaturaViewSet, 
    AsignaturaDocenteGrupoViewSet, EstudianteAsignaturaCursoGradoViewSet, RegistroUsuarioView
    )

router = DefaultRouter()
router.register(r'docentes', DocenteViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'grados', GradoViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'asignaturas', AsignaturaViewSet)
router.register(r'asignatura-docente-grupo', AsignaturaDocenteGrupoViewSet )
router.register(r'estudiante-asignatura-curso-grado', EstudianteAsignaturaCursoGradoViewSet)
router.register(r'registro', RegistroUsuarioView, basename='registro-usuario')

urlpatterns = [
    path('', include(router.urls)),
]
