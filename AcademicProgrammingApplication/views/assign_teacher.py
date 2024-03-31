from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from AcademicProgrammingApplication.models import Class, Teacher


# This function assigns a teacher to a class.
def assign_teacher(request):
    user = request.user
    # Get the value of the 'search' parameter from the GET request
    queryset = request.GET.get('search')
    # Filter teachers who are in the 'Active' state
    teachers = Teacher.objects.filter(state='Activo')
    # If there's a queryset, reassign 'teachers' to filter by name containing 'queryset'
    if queryset:
        teachers = Teacher.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
    # Return the 'assign-teacher.html' template with the provided context
    return render(request, 'assign-teacher.html', {
        'user_name': user.username,
        'title': 'Asignar Profesor a Clase',
        'teacher': teachers.first(),
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
    # Get a list of dictionaries of classes filtered by the teacher's ID
    classes = list(Class.objects.filter(teacher_id=teacher_id).values())
    # If classes are found, return a dictionary with a success message and the classes.
    if len(classes) > 0:
        data = {'messages': "Success", 'clases': classes}
    # If no classes are found, return a dictionary with a not found message.
    else:
        data = {'messages': "Not found"}
    # Return the data as a JSON response
    return JsonResponse(data)
