from django.db import models
from .Teacher import Teacher


class Viatic(models.Model):
    # ATTRIBUTES
    transport = models.BooleanField(null=False, blank=False, verbose_name="Transporte")
    accommodation = models.BooleanField(null=False, blank=False, verbose_name="Alojamiento")
    viatic = models.BooleanField(null=False, blank=False, verbose_name="Viático")
    VIATIC_STATUS_CHOICES = [
        ('ENVIADA', 'Enviada'),
        ('NO_ENVIADA', 'No Enviada'),
    ]
    viatic_status = models.CharField(max_length=200, null=False, blank=False, choices=VIATIC_STATUS_CHOICES,
                                     default='NO_ENVIADO', verbose_name="Estado del viático")

    # RELATIONS
    id_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False, blank=False,
                                   verbose_name="Profesor asociado")

    def __str__(self):
        transport = "Sí" if self.transport else "No"
        accommodation = "Sí" if self.accommodation else "No"
        viatic = "Sí" if self.viatic else "No"
        return f'Transporte: {transport}, Alojamiento: {accommodation}, Viático: {viatic}, Estado del viático: {self.get_viatic_status_display()}'
