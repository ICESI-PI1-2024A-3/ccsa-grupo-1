from django.apps import AppConfig


class AcademicProgrammingApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AcademicProgrammingApplication'

    def ready(self):
        import AcademicProgrammingApplication.signals
