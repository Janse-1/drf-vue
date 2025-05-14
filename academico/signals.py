from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Estudiante, Docente, Coordinador, Padre

@receiver(post_save, sender=Usuario)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        tipo = instance.tipo_usr

        if tipo == 'ESTUDIANTE' and not hasattr(instance, 'estudiante'):
            Estudiante.objects.create(usuario=instance)
        elif tipo == 'DOCENTE' and not hasattr(instance, 'docente'):
            Docente.objects.create(usuario=instance)
        elif tipo == 'COORDINADOR' and not hasattr(instance, 'coordinador'):
            Coordinador.objects.create(usuario=instance)
        elif tipo == 'PADRE' and not hasattr(instance, 'padre'):
            Padre.objects.create(usuario=instance)
