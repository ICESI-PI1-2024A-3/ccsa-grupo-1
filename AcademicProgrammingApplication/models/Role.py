from django.db import models


class Role(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return self.name
