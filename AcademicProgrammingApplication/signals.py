from django.contrib.auth.models import Group
from AcademicProgrammingApplication.models.User import User
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.role:
            group_name = f'{instance.role}'
            group = Group.objects.get(name=group_name)
            instance.groups.add(group)
