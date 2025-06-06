# Generated by Django 5.2.1 on 2025-05-23 22:00

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnioAcademico',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('anio', models.IntegerField(unique=True)),
                ('activo', models.BooleanField(default=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('area', 'Área'), ('subarea', 'Subárea')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('tipo_documento', models.CharField(max_length=5)),
                ('numero_documento', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=200)),
                ('fecha_nacimiento', models.DateField()),
                ('estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grado',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
                ('representacion', models.CharField(max_length=10)),
                ('anio', models.IntegerField()),
                ('cantidad_grupos', models.IntegerField()),
                ('cantidad_asignaturas', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('codigo_dane', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=10)),
                ('cantidad_estudiantes', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('director', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academico.docente')),
                ('grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.grado')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('tipo_documento', models.CharField(max_length=5)),
                ('numero_documento', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=200)),
                ('fecha_nacimiento', models.DateField()),
                ('estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo'), ('graduado', 'Graduado')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('grupo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academico.grupo')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodoAcademico',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('representacion', models.CharField(max_length=10)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('activo', models.BooleanField(default=False)),
                ('anio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodos', to='academico.anioacademico')),
            ],
            options={
                'unique_together': {('anio', 'representacion')},
            },
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('actividad', 'Actividad'), ('examen_final', 'Examen Final')], max_length=20)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('ponderacion', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.asignatura')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.grupo')),
                ('periodo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='academico.periodoacademico')),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nota', models.DecimalField(decimal_places=2, max_digits=5)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.estudiante')),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.evaluacion')),
                ('periodo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='academico.periodoacademico')),
            ],
        ),
        migrations.AddField(
            model_name='grado',
            name='sede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.sede'),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_usr', models.CharField(choices=[('rector', 'Rector'), ('coordinador', 'Coordinador'), ('docente', 'Docente'), ('estudiante', 'Estudiante')], max_length=20)),
                ('activo', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rector',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo_documento', models.CharField(max_length=5)),
                ('numero_documento', models.CharField(max_length=20)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('sexo', models.CharField(max_length=1)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sede', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academico.sede')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academico.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='estudiante',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academico.usuario'),
        ),
        migrations.AddField(
            model_name='docente',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academico.usuario'),
        ),
        migrations.CreateModel(
            name='Coordinador',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo_documento', models.CharField(max_length=5)),
                ('numero_documento', models.CharField(max_length=20)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('sexo', models.CharField(max_length=1)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academico.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='EstudianteAsignaturaCursoGrado',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.asignatura')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.estudiante')),
                ('grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.grado')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.grupo')),
            ],
            options={
                'unique_together': {('estudiante', 'asignatura', 'grupo', 'grado')},
            },
        ),
        migrations.CreateModel(
            name='AsignaturaDocenteGrupo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.asignatura')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.docente')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.grupo')),
            ],
            options={
                'unique_together': {('grupo', 'asignatura')},
            },
        ),
        migrations.CreateModel(
            name='NotaFinal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nota_final', models.DecimalField(decimal_places=2, max_digits=5)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.asignatura')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.estudiante')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.grupo')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.periodoacademico')),
            ],
            options={
                'unique_together': {('estudiante', 'asignatura', 'grupo', 'periodo')},
            },
        ),
        migrations.CreateModel(
            name='DocenteSede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.docente')),
                ('sede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.sede')),
            ],
            options={
                'unique_together': {('docente', 'sede')},
            },
        ),
        migrations.CreateModel(
            name='CoordinadorSede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.coordinador')),
                ('sede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.sede')),
            ],
            options={
                'unique_together': {('coordinador', 'sede')},
            },
        ),
    ]
