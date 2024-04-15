from django.db import models
from .Teacher import Teacher


class Viatic(models.Model):
    # ATTRIBUTES
    transport = models.BooleanField(null=False, blank=False, verbose_name="Transporte")
    accommodation = models.BooleanField(null=False, blank=False, verbose_name="Alojamiento")
    viatic = models.BooleanField(null=False, blank=False, verbose_name="Viático")

    # RELATIONS
    id_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, primary_key=True, null=False, blank=False,
                                      verbose_name="Profesor asociado")  # A teacher can have per diem associated
    # with it and a per diem must be associated with a teacher

    def __str__(self):
        transport = "Sí" if self.transport else "No"
        accommodation = "Sí" if self.accommodation else "No"
        viatic = "Sí" if self.viatic else "No"
        return f'Transporte: {transport}, Alojamiento: {accommodation}, Viático: {viatic}'
