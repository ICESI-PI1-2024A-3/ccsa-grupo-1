# Generated by Django 5.0.3 on 2024-04-20 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AcademicProgrammingApplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='state',
            field=models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')], default='Activo', max_length=200, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='program',
            name='type',
            field=models.CharField(choices=[('ESPECIALIZACIÓN', 'Especialización'), ('MAESTRÍA', 'Maestría'), ('DOCTORADO', 'Doctorado')], max_length=200, verbose_name='Tipo de programa'),
        ),
        migrations.AlterField(
            model_name='viatic',
            name='id_teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='AcademicProgrammingApplication.teacher', verbose_name='Profesor asociado'),
        ),
    ]
