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

def assign_teacher(request):
    queryset = request.GET.get('search')
    teachers = Teacher.objects.filter(state='Activo')

    if queryset:
        teachers = Teacher.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()

    return render(request, 'assign-teacher.html', {
         'user_name': "Carlos",
         'title': 'Asignar Profesor a Clase',
         'teacher': teachers.first(),
     })


# Auto Suggestion of teachers
def search_teacher(request):
    # Get the value of the 'term' parameter from the GET request
    queryset = request.GET.get('term')
    # Filter teachers whose names contain the value of 'queryset'
    teachers = Teacher.objects.filter(
        name__icontains = queryset,
        state = 'Activo'
    ).distinct().values_list('id', 'name')
    # Create a list of results in JSON format
    results = [{'value': teacher[0], 'label': teacher[1]} for teacher in teachers]
    # Returns the results as a JSON response
    return JsonResponse(results, safe=False)