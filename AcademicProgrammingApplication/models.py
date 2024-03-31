from django.db import models
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError


# Create your models here.
class Semester(models.Model):
    # ATTRIBUTES
    period = models.CharField(primary_key=True, max_length=10, null=False, blank=False,
                              verbose_name="Cohorte del semestre")
    start_date = models.DateField(null=False, blank=False, verbose_name="Fecha de inicio")
    ending_date = models.DateField(null=False, blank=False, verbose_name="Fecha de finalización")

    def __str__(self):
        return self.period


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
                                       verbose_name="Semestres asociados")  # A program can be associated with many semesters and a semester can be related to many programs
    subjects = models.ManyToManyField(Subject,
                                      verbose_name="Materias de programas")  # A program can be associated with many subjects and a subject can be related to many programs

    def __str__(self):
        return self.name


class Teacher(models.Model):
    # ATTRIBUTES
    id = models.CharField(primary_key=True, max_length=200, null=False, blank=False,
                          verbose_name="Número de identificación")
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Profesor")
    email = models.EmailField(null=False, blank=False, verbose_name="Correo electrónico")
    cellphone = models.CharField(max_length=20, null=False, blank=False, verbose_name="Teléfono celular")
    city = models.CharField(max_length=200, null=False, blank=False, verbose_name="Ciudad")
    STATES_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    state = models.CharField(max_length=200, choices=STATES_CHOICES, default='Activo', null=False, blank=False,
                             verbose_name="Estado")
    picture = models.ImageField(upload_to='pictures/', null=False, blank=False, verbose_name="Foto del profesor")

    def __str__(self):
        return self.name


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

    # RELATIONS
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                verbose_name="Materia asociada")  # A subject is related to many classes, but a class only to one subject
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                verbose_name="Profesor asociado")  # A teacher can teach many classes, but a class can only have one teacher

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


class Contract(models.Model):
    # ATTRIBUTES
    CONTRACT_STATUS_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    contract_status = models.CharField(max_length=200, null=False, blank=False, choices=CONTRACT_STATUS_CHOICES,
                                       verbose_name="Estado del contrato")
    contact_preparation_date = models.DateField(null=False, blank=False, verbose_name="Fecha de elaboración")

    # RELATIONS
    id_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, primary_key=True, null=False, blank=False,
                                      verbose_name="Profesor asociado")  # A teacher must have a contract and a contract must be associated with a teacher

    def __str__(self):
        return self.id


class Viatic(models.Model):
    # ATTRIBUTES
    transport = models.BooleanField(null=False, blank=False, verbose_name="Transporte")
    accommodation = models.BooleanField(null=False, blank=False, verbose_name="Alojamiento")
    viatic = models.BooleanField(null=False, blank=False, verbose_name="Viático")

    # RELATIONS
    id_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, primary_key=True, null=False, blank=False,
                                      verbose_name="Profesor asociado")  # A teacher can have per diem associated with it and a per diem must be associated with a teacher

    def __str__(self):
        transport = "Sí" if self.transport else "No"
        accommodation = "Sí" if self.accommodation else "No"
        viatic = "Sí" if self.viatic else "No"
        return f'Transporte: {transport}, Alojamiento: {accommodation}, Viático: {viatic}'
