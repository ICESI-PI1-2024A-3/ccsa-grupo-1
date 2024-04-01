from django.shortcuts import render
from AcademicProgrammingApplication.models import Class


def edit_info_class(request, class_id):
    """
    Renders a page for editing class information.

    Parameters:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class to be edited.

    Returns:
        HttpResponse: Rendered HTML page for editing class information.
    """
    # Retrieve the authenticated user
    user = request.user
    # Get the class
    edit_class = Class.objects.filter(id=class_id).first()
    # Render the edit-info-class page with necessary context data
    return render(request, 'edit-info-class.html', {
        'user_name': user.username,
        'title': 'Gestión de clases',
        'class': edit_class,
    })
