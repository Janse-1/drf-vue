from django.contrib import admin
from .models import (
    Usuario, Sede, Rector, Coordinador, CoordinadorSede, Docente, Estudiante,
    Grupo, Grado, Asignatura, Evaluacion, Calificacion, NotaFinal, DocenteSede,
    AsignaturaDocenteGrupo,  EstudianteAsignaturaCursoGrado,
    PeriodoAcademico, AnioAcademico
)

admin.site.register(Usuario)
admin.site.register(Sede)
admin.site.register(Rector)
admin.site.register(Coordinador)
admin.site.register(CoordinadorSede)
admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Grupo)
admin.site.register(Grado)
admin.site.register(Asignatura)
admin.site.register(Evaluacion)
admin.site.register(Calificacion)
admin.site.register(NotaFinal)
admin.site.register(DocenteSede)
admin.site.register(AsignaturaDocenteGrupo)
admin.site.register(EstudianteAsignaturaCursoGrado)
admin.site.register(PeriodoAcademico)
admin.site.register(AnioAcademico)
