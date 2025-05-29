import uuid
from django.contrib.auth.models import User
from django.db import models

#Tabla de los usuarios que maneja django con adiciones para manejar los diferentes
#roles
class Usuario(models.Model):
    TIPO_USUARIO = [
        ('rector', 'Rector'),
        ('coordinador', 'Coordinador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    tipo_usr = models.CharField(max_length=20, choices=TIPO_USUARIO)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#Guardar la información de las sedes de la institución
class Sede(models.Model):
    codigo_dane = models.CharField(max_length=20, primary_key=True) #no se tiene su id, estarán identificadas con su codigo del dane
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

#Información del rector, para que pueda gestionar todas las sedes de la institución
class Rector(models.Model):
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
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
#Guarda la información de los diiferentes coordinadores que tiene cada sede y colegio
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
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#Relacionamos al coordinador con una sede, esta sede es la que tenga a cargo y gestionarla
class CoordinadorSede(models.Model):
    coordinador = models.ForeignKey(Coordinador, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('coordinador', 'sede')


#Guardamos la información para todos los docentes
class Docente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=5)
    numero_documento = models.CharField(max_length=20)
    correo = models.EmailField()
    sexo = models.CharField(max_length=1)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#Relación entre un docente y una sede para saber en que sede imparte clases
class DocenteSede(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('docente', 'sede')

#Crear o identificar los ditintos tipos de grado y relacionarlo a que sede pertenece ese grado
#Ejemplo: Sede principal - 11,10,9..
#Sede secundaria - 3,2,1..
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


#los grupos de cada grado, ejemplo grado 11: 11A, 11B, 11C
class Grupo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=10)
    cantidad_estudiantes = models.IntegerField()
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    director = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#La información de los estudiantes y su estado, y relacionarlo a un grupo
class Estudiante(models.Model):
    ESTADO_CHOICES = [('activo', 'Activo'), ('inactivo', 'Inactivo'), ('graduado', 'Graduado')]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    tipo_documento = models.CharField(max_length=5)
    numero_documento = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    sexo = models.CharField(max_length=1)
    direccion = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, related_name="estudiantes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#Las asignaturas que son impartidas en toda la institución e identificar si pertenecen a área o subarea
#Ejemplo: Matematica: Área 
#Geometría: Subarea
class Asignatura(models.Model):
    TIPO = [('area', 'Área'), ('subarea', 'Subárea')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO)

    def __str__(self):
        return self.nombre


#Relacionar al docente que imparte una asignatura en especifico
class AsignaturaDocenteGrupo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('grupo', 'asignatura')


#Una relacion entre los estudiantes para saber a cual materia, de que grado y grupo pertenecen
class EstudianteAsignaturaCursoGrado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('estudiante', 'asignatura', 'grupo', 'grado')


#Para saber el año actual o si ha iniciado un nuevo año escolar
class AnioAcademico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anio = models.IntegerField(unique=True)
    activo = models.BooleanField(default=False)  # Solo uno puede estar activo a la vez
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return str(self.anio)


#Saber en que periodo academico se está y saber cuando termina o inicia otro
class PeriodoAcademico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anio = models.ForeignKey(AnioAcademico, on_delete=models.CASCADE, related_name='periodos')
    nombre = models.CharField(max_length=50)  # Ejemplo: "Primer Periodo"
    representacion = models.CharField(max_length=10)  # Ej: "P1"
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=False)  # Solo uno por año puede estar activo

    class Meta:
        unique_together = ('anio', 'representacion')

    def __str__(self):
        return f"{self.nombre} ({self.anio.anio})"


#Se guarda la nota final obtenida por un estudiante y a que asignatura, grupo y periodo pertenece esa nota
class NotaFinal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    nota_final = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('estudiante', 'asignatura', 'grupo', 'periodo')
        

#Para guardar las diferentes calificaciones y hacer un historial de las notas detalladas
class Evaluacion(models.Model):
    TIPO = [('actividad', 'Actividad'), ('examen_final', 'Examen Final')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=20, choices=TIPO)
    nombre = models.CharField(max_length=100)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha = models.DateField()
    ponderacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE, null=True)

#Para guardar todas esas notas obtenidas en cada evaluación
class Calificacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE, null=True)