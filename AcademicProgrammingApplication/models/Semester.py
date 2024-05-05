from django.db import models


# Create your models here.
class Semester(models.Model):
    # ATTRIBUTES
    period = models.CharField(primary_key=True, max_length=10, null=False, blank=False,
                              verbose_name="Cohorte del semestre")
    start_date = models.DateField(null=False, blank=False, verbose_name="Fecha de inicio")
    ending_date = models.DateField(null=False, blank=False, verbose_name="Fecha de finalización")

    def __str__(self):
        return self.period
