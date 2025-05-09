import uuid
from django.db import models

class Usuario(models.Model):
    TIPO_USUARIO = [
        ('coordinador', 'Coordinador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
        ('padre', 'Padre'),
    ]
    id_usr = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario_usr = models.CharField(max_length=50, unique=True)
    contrasena_usr = models.CharField(max_length=255)
    tipo_usr = models.CharField(max_length=20, choices=TIPO_USUARIO)
    activo_usr = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Sede(models.Model):
    codigo_dane_sed = models.CharField(max_length=12, primary_key=True)
    nombre_sed = models.CharField(max_length=100)
    direccion_sed = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Coordinador(models.Model):
    id_coo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_documento_coo = models.CharField(max_length=5)
    numero_documento_coo = models.CharField(max_length=20)
    nombres_coo = models.CharField(max_length=50)
    apellidos_coo = models.CharField(max_length=50)
    sexo_coo = models.CharField(max_length=1)
    telefono_coo = models.CharField(max_length=20)
    correo_coo = models.EmailField()
    direccion_coo = models.CharField(max_length=100)
    fecha_nacimiento_coo = models.DateField()
    sede_codigo_dane = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Docente(models.Model):
    id_doc = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_documento_doc = models.CharField(max_length=5)
    numero_documento_doc = models.CharField(max_length=20)
    nombres_doc = models.CharField(max_length=50)
    apellidos_doc = models.CharField(max_length=50)
    sexo_doc = models.CharField(max_length=1)
    telefono_doc = models.CharField(max_length=20)
    estado_doc = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    direccion_doc = models.CharField(max_length=100)
    fecha_nacimiento_doc = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DocenteSede(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('docente', 'sede')

class Grado(models.Model):
    id_gra = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_gra = models.CharField(max_length=20)
    representacion_gra = models.CharField(max_length=10)
    anio_gra = models.IntegerField()
    cantidad_grupos_gra = models.IntegerField()
    cantidad_asignaturas_gra = models.IntegerField()
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Grupo(models.Model):
    id_grp = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_grp = models.CharField(max_length=10)
    cantidad_estudiantes_grp = models.IntegerField()
    id_grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    director_grupo = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Estudiante(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('graduado', 'Graduado')
    ]
    id_est = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_documento_est = models.CharField(max_length=5)
    numero_documento_est = models.CharField(max_length=20)
    nombres_est = models.CharField(max_length=50)
    apellidos_est = models.CharField(max_length=50)
    sexo_est = models.CharField(max_length=1)
    direccion_est = models.CharField(max_length=100)
    fecha_nacimiento_est = models.DateField()
    estado_est = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Padre(models.Model):
    id_pad = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres_pad = models.CharField(max_length=50)
    apellidos_pad = models.CharField(max_length=50)
    correo_pad = models.EmailField()
    telefono_pad = models.CharField(max_length=20)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class PadreEstudiante(models.Model):
    padre = models.ForeignKey(Padre, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('padre', 'estudiante')

class Asignatura(models.Model):
    TIPO_ASIG = [('area', 'Área'), ('subarea', 'Subárea')]
    id_asig = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_asig = models.CharField(max_length=100)
    tipo_asig = models.CharField(max_length=10, choices=TIPO_ASIG)
    id_area = models.UUIDField(null=True, blank=True)  # Puede ser clave foránea si referencian áreas

class AsignaturaDocenteGrupo(models.Model):
    id_adg = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    id_docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

class EstudianteAsignaturaCursoGrado(models.Model):
    id_est_asig = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)

class Evaluacion(models.Model):
    TIPO_EVAL = [('actividad', 'Actividad'), ('disciplina', 'Disciplina'), ('examen_final', 'Examen Final')]
    id_eval = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_eval = models.CharField(max_length=20, choices=TIPO_EVAL)
    nombre_eval = models.CharField(max_length=100)
    id_asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_eval = models.DateField()
    ponderacion_eval = models.DecimalField(max_digits=5, decimal_places=2)

class Calificacion(models.Model):
    id_cal = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    calificacion_cal = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones_cal = models.TextField(blank=True, null=True)

class Asistencia(models.Model):
    id_asi = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_asi = models.DateField()

class AsistenciaEstudiante(models.Model):
    ESTADO_AE = [('presente', 'Presente'), ('ausente', 'Ausente'), ('excusado', 'Excusado')]
    id_ae = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_asistencia = models.ForeignKey(Asistencia, on_delete=models.CASCADE)
    id_estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    estado_ae = models.CharField(max_length=10, choices=ESTADO_AE)
    observaciones_ae = models.TextField(blank=True, null=True)

class EvaluacionAspecto(models.Model):
    id_eva = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_eva = models.CharField(max_length=50)
    ponderacion_eva = models.DecimalField(max_digits=5, decimal_places=2)

class PeriodoAcademico(models.Model):
    id_per = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_per = models.CharField(max_length=50)
    representacion_per = models.CharField(max_length=10)
