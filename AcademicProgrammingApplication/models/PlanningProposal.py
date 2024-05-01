from django.db import models


class PlanningProposal(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, default="none")
    name_file = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    path = models.FileField(upload_to='files/', default='BasePlanningAcademicProgramming.xlsx')

    def __str__(self):
        return self.name_file
