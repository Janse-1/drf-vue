from django.contrib import admin
from .models import (
    Usuario, Sede, Coordinador, Docente, Estudiante,
    Padre, Grupo, Grado, Asignatura, Evaluacion, Calificacion,
    Asistencia, AsistenciaEstudiante, DocenteSede,
    AsignaturaDocenteGrupo, PadreEstudiante, EstudianteAsignaturaCursoGrado,
    EvaluacionAspecto, PeriodoAcademico
)

admin.site.register(Usuario)
admin.site.register(Sede)
admin.site.register(Coordinador)
admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Padre)
admin.site.register(Grupo)
admin.site.register(Grado)
admin.site.register(Asignatura)
admin.site.register(Evaluacion)
admin.site.register(Calificacion)
admin.site.register(Asistencia)
admin.site.register(AsistenciaEstudiante)
admin.site.register(DocenteSede)
admin.site.register(AsignaturaDocenteGrupo)
admin.site.register(PadreEstudiante)
admin.site.register(EstudianteAsignaturaCursoGrado)
admin.site.register(EvaluacionAspecto)
admin.site.register(PeriodoAcademico)
