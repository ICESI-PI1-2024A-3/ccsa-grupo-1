# Import necessary modules
from django.db.models import Q
from django.shortcuts import render, redirect

from AcademicProgrammingApplication.models import Semester, Program


# Define a view function for managing academic programming
def academic_management(request):
    """
    View function for managing academic programming.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page displaying academic management information.
    """
    # Retrieve the authenticated user
    user = request.user

    # Get query parameters from the request
    queryset = request.GET

    # Initialize variables
    program_information = None
    semester = None
    subjects = request.GET.get('subject_search')

    # Check if query parameters exist
    if queryset:
        try:
            # Extract program and semester from query parameters
            program = queryset.get('program')
            semester = Semester.objects.get(period=queryset.get('semester'))

            # Query the database for program information based on program name and semester
            program_information = Program.objects.filter(
                Q(name__icontains=program) & Q(semesters__in=[semester])).first()

            # Filter subjects based on search query or retrieve all subjects for the program
            if subjects:
                subjects = program_information.subjects.filter(name__icontains=subjects).distinct()
            else:
                subjects = program_information.subjects.all()

        except Exception:
            # Render error message if program or semester is not found
            return render(request, 'academic-management.html', {
                'title': 'Programación académica',
                'change_role_permission': user.has_perm('AcademicProgrammingApplication.change_role'),
                'user_name': user.username,
                'user_role': user.role,
                'error': 'Lo sentimos, no fue posible encontrar el programa o semestre que estás buscando. Por favor, '
                         'verifica que la información ingresada sea correcta e intentalo nuevamente.',
            })

    request.session['program_search_url'] = request.build_absolute_uri()

    # Render the academic management page with necessary context data
    return render(request, 'academic-management.html', {
        'title': 'Programación académica',
        'change_role_permission': user.has_perm('AcademicProgrammingApplication.change_role'),
        'delete_program_permission': user.has_perm('AcademicProgrammingApplication.delete_program'),
        'user_name': user.username,
        'user_role': user.role,
        'program_information': program_information,
        'semester': semester,
        'subjects': subjects,
    })


# Define a view function for deleting an academic program
def delete_academic_program(request, program_id):
    """
    Deletes an academic program.

    Parameters:
        request (HttpRequest): The HTTP request object.
        program_id (int): The ID of the program to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the home page.
    """
    # Retrieve the program instance to be deleted
    program = Program.objects.get(id=program_id)

    # Delete the program
    program.delete()

    # Redirect the user to the home page
    return redirect('home')


def academic_program_edition(request, program_id):
    """
    Renders a page for editing an academic program.

    Parameters:
        request (HttpRequest): The HTTP request object.
        program_id (int): The ID of the program to be edited.

    Returns:
        HttpResponse: Rendered HTML page for program editing.
    """
    # Retrieve the authenticated user
    user = request.user
    program = Program.objects.get(id=program_id)
    modalities = Program.objects.values_list('modality', flat=True).distinct()
    types = Program.objects.values_list('type', flat=True).distinct()

    return render(request, 'academic-program-edition.html', {
        'title': 'Programación académica',
        'change_role_permission': user.has_perm('AcademicProgrammingApplication.change_role'),
        'user_name': user.username,
        'user_role': user.role,
        "program": program,
        "modalities": modalities,
        "types": types,
    })


def edit_academic_program(request, program_id):
    """
    Handles the editing of an academic program.

    Parameters:
        request (HttpRequest): The HTTP request object.
        program_id (int): The ID of the program to be edited.

    Returns:
        HttpResponseRedirect: Redirects to the previous page.
    """
    try:
        name = request.POST.get('name')
        program_type = request.POST.get('type')
        faculty = request.POST.get('faculty')
        modality = request.POST.get('modality')
        program_manager = request.POST.get('program_manager')
        duration = request.POST.get('duration')
        cost = request.POST.get('cost')
        curriculum = request.FILES.get('curriculum')

        program = Program.objects.get(id=program_id)
        program.name = name
        program.type = program_type
        program.faculty = faculty
        program.modality = modality
        program.director = program_manager
        program.duration = int(duration)
        program.cost = cost
        if curriculum:
            program.curriculum = request.FILES['curriculum']
        program.save()
        return redirect(request.session.get('program_search_url', 'home'))
    except Exception as e:
        # In case of error, it sends a failure response.
        print(e)
        return redirect('home')
