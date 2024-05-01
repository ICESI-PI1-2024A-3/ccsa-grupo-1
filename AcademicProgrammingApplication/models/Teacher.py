from django.db import models


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
