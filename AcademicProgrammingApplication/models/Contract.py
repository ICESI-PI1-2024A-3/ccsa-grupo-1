from django.db import models
from .Teacher import Teacher


class Contract(models.Model):
    # ATTRIBUTES
    id = models.CharField(primary_key=True, max_length=200, null=False, blank=False, verbose_name="Identificador del contrato")
    CONTRACT_STATUS_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    contract_status = models.CharField(max_length=200, null=False, blank=False, choices=CONTRACT_STATUS_CHOICES,
                                       verbose_name="Estado del contrato")
    contact_preparation_date = models.DateField(null=False, blank=False, verbose_name="Fecha de elaboración")

    # RELATIONS
    id_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=False, blank=False,
                                      verbose_name="Profesor asociado")  # A teacher must have a contract and a
    # contract must be associated with a teacher

    def __str__(self):
        return self.id
