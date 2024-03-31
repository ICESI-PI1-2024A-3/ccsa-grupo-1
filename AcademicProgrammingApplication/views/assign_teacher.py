from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from AcademicProgrammingApplication.models import Class, Teacher


# This function assigns a teacher to a class.
def assign_teacher(request, class_id):
    user = request.user
    # Get the class to assign
    new_class = Class.objects.filter(id=class_id).first()
    new_class_formatted = {
        'title': new_class.subject.name,
        'start': new_class.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
        'end': new_class.ending_date.strftime('%Y-%m-%dT%H:%M:%S')
    }
    # Get the value of the 'search' parameter from the GET request
    queryset = request.GET.get('search')
    # Filter teachers who are in the 'Active' state
    teachers = Teacher.objects.filter(state='Activo')
    # If there's a queryset, reassign 'teachers' to filter by name containing 'queryset'
    if queryset:
        teachers = Teacher.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
    # Get the teacher searched
    teacher = teachers.first()
    # Check for overlapping classes
    overlapping_classes = Class.objects.filter(
        teacher=teacher,
        start_date__lt=new_class.ending_date,
        ending_date__gt=new_class.start_date
    )
    # If there are overlapping classes, show an alert
    if overlapping_classes.exists():
        return render(request, 'assign-teacher.html', {
            'user_name': user.username,
            'title': 'Asignar Profesor a Clase',
            'teacher': teacher,
            'classes': get_classes(request, teacher),
            'new_class': new_class_formatted,
            'overlap_alert': True,
        })
    # If there are no overlapping classes, proceed with assigning the class
    else:
        return render(request, 'assign-teacher.html', {
            'user_name': user.username,
            'title': 'Asignar Profesor a Clase',
            'teacher': teacher,
            'classes': get_classes(request, teacher),
            'new_class': new_class_formatted,
        })


# Function to search for teachers based on an entered term.
def search_teacher(request):
    # Get the value of the 'term' parameter from the GET request
    queryset = request.GET.get('term')
    # Filter teachers whose names contain the value of 'queryset'
    teachers = Teacher.objects.filter(
        name__icontains=queryset,
        state='Activo'
    ).distinct().values_list('id', 'name')
    # Create a list of results in JSON format
    results = [{'value': teacher[0], 'label': teacher[1]} for teacher in teachers]
    # Returns the results as a JSON response
    return JsonResponse(results, safe=False)


# Get the classes associated with a given teacher ID
def get_classes(_request, teacher_id):
    # Get the classes associated with a given teacher
    classes = Class.objects.filter(teacher_id=teacher_id).all()
    # Initialize the array of out
    out = []
    # Get the information most important of the classes
    for session in classes:
        out.append({
            'title': session.subject.name,
            'start': session.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': session.ending_date.strftime('%Y-%m-%dT%H:%M:%S')
        })
    return out
