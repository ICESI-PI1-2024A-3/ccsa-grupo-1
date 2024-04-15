from django.db import models
from django.core.validators import FileExtensionValidator


class Subject(models.Model):
    # ATTRIBUTES
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Materia")
    nrc = models.CharField(max_length=200, null=False, blank=False, verbose_name="NRC")
    credits = models.PositiveIntegerField(null=False, blank=False, verbose_name="Número de créditos")
    TYPE_CHOICES = [
        ('CURRICULAR', 'Curricular'),
        ('ELECTIVA', 'Electiva'),
    ]
    type = models.CharField(max_length=200, choices=TYPE_CHOICES, null=False, blank=False, verbose_name="Tipo")
    syllabus = models.FileField(upload_to='syllabuses/',
                                validators=[FileExtensionValidator(['pdf'])],
                                error_messages={'invalid_extension': 'Por favor, suba el archivo en formato .PDF'},
                                verbose_name="Syllabus")
    start_date = models.DateField(null=False, blank=False, verbose_name="Fecha de inicio")
    ending_date = models.DateField(null=False, blank=False, verbose_name="Fecha de finalización")
    MODALITY_CHOICES = [
        ('PRESENCIAL', 'Presencial'),
        ('VIRTUAL', 'Virtual'),
    ]
    modality = models.CharField(max_length=200, choices=MODALITY_CHOICES, null=False, blank=False,
                                verbose_name="Modalidad de la materia")
    num_sessions = models.PositiveIntegerField(null=False, blank=False, verbose_name="Cantidad de sesiones")

    def __str__(self):
        return self.name
