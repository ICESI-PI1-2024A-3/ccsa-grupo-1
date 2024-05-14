from django.shortcuts import render
from AcademicProgrammingApplication.models import Teacher, Contract


def teacher_management(request):
    """
    Renders a page for managing teachers.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page displaying teacher management information.
    """
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
        'change_role_permission': user.has_perm('AcademicProgrammingApplication.change_role'),
        'user_name': user.username,
        'user_role': user.role,
        'teachers': teachers
    })
