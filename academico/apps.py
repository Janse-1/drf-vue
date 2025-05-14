from django.apps import AppConfig


class AcademicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'academico'
    
    
    def ready(self):
     import academico.signals
    

