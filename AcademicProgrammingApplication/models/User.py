from django.contrib.auth.models import AbstractUser
from django.db import models
from .Role import Role


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
