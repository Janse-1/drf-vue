from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocenteViewSet, EstudianteViewSet, GradoViewSet, GrupoViewSet, AsignaturaViewSet

router = DefaultRouter()
router.register(r'docentes', DocenteViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'grados', GradoViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'asignaturas', AsignaturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
