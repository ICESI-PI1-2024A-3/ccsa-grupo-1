from django.db import models
from django.core.validators import FileExtensionValidator
from .Semester import Semester
from .Subject import Subject


class Program(models.Model):
    # ATTRIBUTES
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Programa")
    faculty = models.CharField(max_length=200, null=False, blank=False, verbose_name="Facultad academica")
    director = models.CharField(max_length=200, null=False, blank=False, verbose_name="Director de programa")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,
                               verbose_name="Costo de matricula")
    TYPE_CHOICES = [
        ('ESPECIALIZACIÓN', 'Especialización'),
        ('MAESTRÍA', 'Maestría'),
        ('DOCTORADO', 'Doctorado'),
    ]
    type = models.CharField(max_length=200, choices=TYPE_CHOICES, null=False, blank=False,
                            verbose_name="Tipo de programa")
    MODALITY_CHOICES = [
        ('PRESENCIAL', 'Presencial'),
        ('VIRTUAL', 'Virtual'),
    ]
    modality = models.CharField(max_length=200, choices=MODALITY_CHOICES, null=False, blank=False,
                                verbose_name="Modalidad del programa")
    duration = models.CharField(max_length=200, null=False, blank=False, verbose_name="Duración del programa")
    curriculum = models.FileField(upload_to='curriculums/',
                                  validators=[FileExtensionValidator(['pdf'])],
                                  error_messages={'invalid_extension': 'Por favor, suba el archivo en formato .PDF'},
                                  verbose_name="Curriculum del programa")

    # RELATIONS
    semesters = models.ManyToManyField(Semester,
                                       verbose_name="Semestres asociados")  # A program can be associated with many
    # semesters and a semester can be related to many programs
    subjects = models.ManyToManyField(Subject,
                                      verbose_name="Materias de programas")  # A program can be associated with many
    # subjects and a subject can be related to many programs

    def __str__(self):
        return self.name
