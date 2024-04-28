# Generated by Django 5.0.3 on 2024-04-20 01:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AcademicProgrammingApplication', '0002_teacher_state_alter_program_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='viatic',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='viatic',
            name='id_teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AcademicProgrammingApplication.teacher', verbose_name='Profesor asociado'),
        ),
    ]
