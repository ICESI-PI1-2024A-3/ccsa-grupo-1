from django.db import models

class Student(models.Model):
    # Atributos
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Nombre")
    student_id = models.CharField(primary_key=True, max_length=200, null=False, blank=False, verbose_name="ID del estudiante")
    id_type = models.CharField(max_length=100, null=False, blank=False, verbose_name="Tipo de ID")
    email = models.EmailField(null=False, blank=False, verbose_name="Correo electrónico")

    def __str__(self):
        return self.name