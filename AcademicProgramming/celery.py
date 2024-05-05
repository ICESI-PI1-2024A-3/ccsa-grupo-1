from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer la configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AcademicProgramming.settings')

# Crear una instancia de la aplicación Celery
app = Celery('AcademicProgramming')

# Cargar la configuración de Celery desde el archivo de configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir y registrar las tareas de Celery desde todas las aplicaciones de Django
app.autodiscover_tasks()