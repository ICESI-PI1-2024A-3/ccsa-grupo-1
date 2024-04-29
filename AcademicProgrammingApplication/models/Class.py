from django.db import models
from django.forms import ValidationError
from .Subject import Subject
from .Teacher import Teacher
from .Student import Student


class Class(models.Model):
    # ATTRIBUTES
    id = models.CharField(primary_key=True, max_length=10, null=False, blank=False, verbose_name="Número de sesión")
    start_date = models.DateTimeField(null=False, blank=False, verbose_name="Fecha de inicio de la clase")
    ending_date = models.DateTimeField(null=False, blank=False, verbose_name="Fecha de finalización de la clase")
    MODALITY_CHOICES = [
        ('PRESENCIAL', 'Presencial'),
        ('VIRTUAL', 'Virtual'),
    ]
    modality = models.CharField(max_length=200, choices=MODALITY_CHOICES, null=False, blank=False,
                                verbose_name="Modalidad de la clase")
    classroom = models.CharField(max_length=200, null=True, blank=True, verbose_name="Salón de clase")
    link = models.URLField(null=True, blank=True, verbose_name="Enlace de la plataforma virtual")
    send_email = models.BooleanField(default=True, verbose_name="Enviar correo electrónico")

    # RELATIONS
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                verbose_name="Materia asociada")  # A subject is related to many classes, but a class
    # only to one subject
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                verbose_name="Profesor asociado")  # A teacher can teach many classes, but a class
    # can only have one teacher
    students = models.ManyToManyField(Student, related_name='classes', verbose_name="Estudiantes")

    def save(self, *args, **kwargs):
        if self.modality == 'PRESENCIAL':
            if not self.classroom:
                raise ValidationError("Se espera un salón para la modalidad presencial")
            self.link = ""
        else:  # MODALITY is 'VIRTUAL'
            if not self.link:
                raise ValidationError("Se espera un enlace para la modalidad virtual")
            self.classroom = ""
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id
