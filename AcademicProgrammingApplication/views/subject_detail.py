from django.shortcuts import render
from AcademicProgrammingApplication.models import Subject, Class


def subject_detail(request, subject_id):
    user = request.user
    subject = Subject.objects.get(code=subject_id)
    classes = Class.objects.filter(subject=subject)  # Obtiene todas las clases relacionadas con la materia
    return render(request, 'subject_detail.html',
                  {'user_name': user.username, 'subject': subject, 'classes': classes, 'title': 'Gestión de MATERIA'})
