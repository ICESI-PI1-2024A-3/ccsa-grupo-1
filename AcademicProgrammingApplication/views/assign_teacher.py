from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from AcademicProgrammingApplication.models import Class, Teacher

def assign_teacher(request, class_id):
    """
    Assigns a teacher to a class.
    
    Parameters:
        request: HttpRequest object.
        class_id (str): The ID of the class to assign a teacher to.
        
    Returns:
        HttpResponse: Rendered template with assigned teacher information.
    """
    # Retrieve the authenticated user
    user = request.user
    # Get the class to assign
    new_class = Class.objects.filter(id=class_id).first()
    new_class_formatted = {
        'id': new_class.id,
        'title': new_class.subject.name,
        'start': new_class.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
        'end': new_class.ending_date.strftime('%Y-%m-%dT%H:%M:%S')
    }
    # Get the value of the 'search' parameter from the GET request
    queryset = request.GET.get('search')
    # Get the teacher assigned to the class
    teacher = new_class.teacher if new_class.teacher else None
    # If there's a queryset, reassign 'teachers' to filter by name containing 'queryset'
    if queryset:
        teachers = Teacher.objects.filter(
            state='Activo',
            name__icontains=queryset
        ).distinct()
        # Get the teacher searched
        teacher = teachers.first()
    # Check for overlapping classes
    overlap_alert = Class.objects.filter(
        teacher=teacher,
        start_date__lt=new_class.ending_date,
        ending_date__gt=new_class.start_date
    ).exclude(id=class_id).exists()
    # Save the teacher's assignment
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        teacher = Teacher.objects.get(id=teacher_id)
        # Assign the class to the teacher
        new_class.teacher = teacher
        new_class.save()
        # Redirect to the edit_info_class page
        return redirect('edit_info_class', class_id=new_class.id)
    
    return render(request, 'assign-teacher.html', {
        'user_name': user.username,
        'title': 'Asignar Profesor a Clase',
        'teacher': teacher,
        'classes': get_classes(teacher, new_class),
        'new_class': new_class_formatted,
        'overlap_alert': overlap_alert,
    })


def search_teacher(request):
    """
    Searches for teachers based on the entered term.
    
    Parameters:
        request: HttpRequest object.
        
    Returns:
        JsonResponse: JSON response containing search results.
    """
    # Get the value of the 'term' parameter from the GET request
    queryset = request.GET.get('term')
    # Filter teachers whose names contain the value of 'queryset'
    teachers = Teacher.objects.filter(
        name__icontains=queryset,
        state='Activo'
    ).distinct().values_list('id', 'name')
    # Create a list of results in JSON format
    results = [{'value': teacher[0], 'label': teacher[1]} for teacher in teachers]
    # Return the results as a JSON response
    return JsonResponse(results, safe=False)


def get_classes(teacher, new_class=None):
    """
    Get the classes associated with a given teacher ID.
    
    Parameters:
        teacher (Teacher): The teacher object.
        new_class (Class, optional): The new class object. Defaults to None.
        
    Returns:
        list: List of dictionaries containing class information.
    """
    # Get the classes associated with a given teacher
    classes = Class.objects.filter(teacher=teacher).exclude(id=new_class.id if new_class else None)
    # Initialize the array of output
    out = []
    # Get the most important information of the classes
    for session in classes:
        out.append({
            'title': session.subject.name,
            'start': session.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': session.ending_date.strftime('%Y-%m-%dT%H:%M:%S')
        })
    return out
