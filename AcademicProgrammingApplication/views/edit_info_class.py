from django.shortcuts import render
from AcademicProgrammingApplication.models import Class


def edit_info_class(request, class_id):
    user = request.user
    # Get the class
    edit_class = Class.objects.filter(id=class_id).first()
    return render(request, 'edit-info-class.html', {
        'user_name': user.username,
        'title': 'Gestión de clases',
        'class': edit_class,
    })
