# Generated by Django 5.0.3 on 2024-05-02 05:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AcademicProgrammingApplication', '0002_student_class_send_email_class_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='id_teacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AcademicProgrammingApplication.teacher', verbose_name='Profesor asociado'),
        ),
    ]