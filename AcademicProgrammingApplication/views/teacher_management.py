from django.shortcuts import render
from AcademicProgrammingApplication.models import Teacher, Contract

def teacher_management(request):
    # Retrieve the authenticated user
    user = request.user
    # Get query parameters from the request
    queryset = request.GET.get('teacher_search', '')
    # Filter teachers based on search query or retrieve all teachers
    if queryset:
        teachers = Teacher.objects.select_related('contract').filter(name__icontains=queryset)
    else:
        teachers = Teacher.objects.select_related('contract').all()
    # Render the teacher management page with necessary context data
    return render(request, 'teacher-management.html', {
        'title': 'Gestión de Profesores',
        'user_name': user.username,
        'teachers': teachers
    })