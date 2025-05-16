import uuid
from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    TIPO_USUARIO = [
        ('coordinador', 'Coordinador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
        ('padre', 'Padre'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    tipo_usr = models.CharField(max_length=20, choices=TIPO_USUARIO)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Sede(models.Model):
    codigo_dane = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Coordinador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_documento = models.CharField(max_length=5)
    numero_documento = models.CharField(max_length=20)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    direccion = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Docente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=5)
    numero_documento = models.CharField(max_length=20)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DocenteSede(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('docente', 'sede')


class Grado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=20)
    representacion = models.CharField(max_length=10)
    anio = models.IntegerField()
    cantidad_grupos = models.IntegerField()
    cantidad_asignaturas = models.IntegerField()
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Grupo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=10)
    cantidad_estudiantes = models.IntegerField()
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    director = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Estudiante(models.Model):
    ESTADO_CHOICES = [('activo', 'Activo'), ('inactivo', 'Inactivo'), ('graduado', 'Graduado')]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    tipo_documento = models.CharField(max_length=5)
    numero_documento = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Padre(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PadreEstudiante(models.Model):
    padre = models.ForeignKey(Padre, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('padre', 'estudiante')


class Asignatura(models.Model):
    TIPO = [('area', 'Área'), ('subarea', 'Subárea')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO)

    def __str__(self):
        return self.nombre


class AsignaturaDocenteGrupo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('grupo', 'asignatura')


class EstudianteAsignaturaCursoGrado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('estudiante', 'asignatura', 'grupo', 'grado')


class Evaluacion(models.Model):
    TIPO = [('actividad', 'Actividad'), ('disciplina', 'Disciplina'), ('examen_final', 'Examen Final')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=20, choices=TIPO)
    nombre = models.CharField(max_length=100)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha = models.DateField()
    ponderacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


class Calificacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)


class Asistencia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha = models.DateField()


class AsistenciaEstudiante(models.Model):
    ESTADO = [('presente', 'Presente'), ('ausente', 'Ausente'), ('excusado', 'Excusado')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asistencia = models.ForeignKey(Asistencia, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO)
    observaciones = models.TextField(blank=True, null=True)


class EvaluacionAspecto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50)
    ponderacion = models.DecimalField(max_digits=5, decimal_places=2)


class PeriodoAcademico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50)
    representacion = models.CharField(max_length=10)
