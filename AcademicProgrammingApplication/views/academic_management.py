from django.shortcuts import render
from django.db.models import Q
from AcademicProgrammingApplication.models import Semester, Program


def academic_management(request):
    user = request.user
    queryset = request.GET
    program = queryset.get('program')
    semester = Semester.objects.get(period=queryset.get('semester'))
    program_information = None
    if queryset:
        program_information = Program.objects.filter(Q(name__icontains=program) & Q(semesters__in=[semester])).first()

    return render(request, 'academic-management.html', {
        'title': 'Programación académica',
        'user_name': user.username,
        'program_information': program_information,
        'semester': semester,
    })
