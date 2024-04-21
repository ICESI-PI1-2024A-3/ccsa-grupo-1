from django.db import models


class Role(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
