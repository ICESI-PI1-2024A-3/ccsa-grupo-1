from django.shortcuts import render
from django.db.models import Q
from AcademicProgrammingApplication.models import Semester, Program


def academic_management(request):
    user = request.user
    queryset = request.GET
    program_information = None
    semester = None
    subjects = request.GET.get('subject_search')
    if queryset:
        try:
            program = queryset.get('program')
            semester = Semester.objects.get(period=queryset.get('semester'))
            program_information = Program.objects.filter(
                Q(name__icontains=program) & Q(semesters__in=[semester])).first()
            if subjects:
                subjects = program_information.subjects.filter(name__icontains=subjects).distinct()
            else:
                subjects = program_information.subjects.all()
        except AttributeError:
            return render(request, 'academic-management.html', {
                'title': 'Programación académica',
                'user_name': user.username,
                'error': 'Lo sentimos, no fue posible encontrar el programa o semestre que estás buscando. Por favor, '
                         'verifica que la información ingresada sea correcta e intentalo nuevamente.',
            })

    return render(request, 'academic-management.html', {
        'title': 'Programación académica',
        'user_name': user.username,
        'program_information': program_information,
        'semester': semester,
        'subjects': subjects,
    })
