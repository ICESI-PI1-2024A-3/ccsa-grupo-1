from django.http import JsonResponse
from django.shortcuts import render
from .forms import UserForm
from .models import Teacher, Class
from django.db.models import Q


# Create your views here.
def login(request):
    # print(request.POST)
    return render(request, 'login.html', {
        'form': UserForm()
    })


# The next lines are only used to see how the base HTML looks like
# def base_screen(request):
#     return render(request, 'layouts/base-app-pages.html', {
#         'user_name': "Carlos",
#         'title': 'Main page',
#     })


# This function assigns a teacher to a class.
def assign_teacher(request):
    # Get the value of the 'search' parameter from the GET request
    queryset = request.GET.get('search')
    # Filter teachers who are in the 'Active' state
    teachers = Teacher.objects.filter(state='Active')

    # If there's a queryset, reassign 'teachers' to filter by name containing 'queryset'
    if queryset:
        teachers = Teacher.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()

    # Return the 'assign-teacher.html' template with the provided context
    return render(request, 'assign-teacher.html', {
        'user_name': "Carlos",
        'title': 'Assign Teacher to Class',
        'teacher': teachers.first(),  # Returns the first found teacher
    })


# Function to search for teachers based on an entered term.
def search_teacher(request):
    # Get the value of the 'term' parameter from the GET request
    queryset = request.GET.get('term')
    # Filter teachers whose names contain the value of 'queryset'
    teachers = Teacher.objects.filter(
        name__icontains=queryset,
        state='Active'
    ).distinct().values_list('id', 'name')
    # Create a list of results in JSON format
    results = [{'value': teacher[0], 'label': teacher[1]} for teacher in teachers]
    # Return the results as a JSON response
    return JsonResponse(results, safe=False)


# Get the classes associated with a given teacher ID
def get_classes(_request, teacher_id):
    # Get a list of dictionaries of classes filtered by the teacher's ID
    classes = list(Class.objects.filter(teacher_id=teacher_id).values())
    print(classes)  # Print the classes to the console
    # If classes are found, return a dictionary with a success message and the classes.
    if (len(classes) > 0):
        data = {'messages': "Success", 'classes': classes}
    # If no classes are found, return a dictionary with a not found message.
    else:
        data = {'messages': "Not found"}

    return JsonResponse(data)  # Return the data as a JSON response