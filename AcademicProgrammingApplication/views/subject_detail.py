from django.shortcuts import render
from AcademicProgrammingApplication.models import Subject, Class


def subject_detail(request, subject_id):
    """
    Renders a page displaying details of a subject and its related classes.

    Parameters:
        request (HttpRequest): The HTTP request object.
        subject_id (str): The code of the subject to be displayed.

    Returns:
        HttpResponse: Rendered HTML page for subject details.
    """
    # Retrieve the authenticated user
    user = request.user
    # Get the subject based on the provided subject_id
    subject = Subject.objects.get(code=subject_id)
    # Get all classes related to the subject
    classes = Class.objects.filter(subject=subject)
    # Render the subject_detail page with necessary context data
    return render(request, 'subject_detail.html',
                  {'user_name': user.username, 'subject': subject, 'classes': classes, 'title': 'Gestión de MATERIA'})
