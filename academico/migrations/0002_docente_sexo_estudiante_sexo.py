# Generated by Django 5.2.1 on 2025-05-24 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='docente',
            name='sexo',
            field=models.CharField(default='N', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estudiante',
            name='sexo',
            field=models.CharField(default='N', max_length=1),
            preserve_default=False,
        ),
    ]
