from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import UserForm
from .models import Subject, Class
from .models import Teacher


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': UserForm()
        })
    else:
        # Method that helps me verify if the data obtained in the login is correct
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': UserForm(),
                'error': 'Nombre de usuario o contraseña incorrectos.',
            })
        else:
            auth_login(request, user)
            return redirect('home')


def subject_detail(request, subject_id):
    subject = Subject.objects.get(code=subject_id)
    classes = Class.objects.filter(subject=subject)  # Obtiene todas las clases relacionadas con la materia
    return render(request, 'subject_detail.html',
                  {'subject': subject, 'classes': classes, 'title': 'Gestión de MATERIA'})


# The next lines are only used to see how the base HTML looks like
def base_screen(request):
    return render(request, 'layouts/base-app-pages.html', {
        'user_name': "User",
        'title': 'Main page',
    })


def academic_management(request):
    user = request.user
    return render(request, 'academic-management.html', {
        'title': 'Programación académica',
        'user_name': user.username,
    })


def sing_up(request):
    if request.method == 'GET':
        return render(request, 'sing-up.html', {
            'form': UserCreationForm,
        })
    else:
        username = request.POST['username']
        if not username:
            return render(request, 'sing-up.html', {
                'form': UserCreationForm,
                'error': '¡Todos los campos son obligatorios!',
            })

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                auth_login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'sing-up.html', {
                    'form': UserCreationForm,
                    'error': '¡El usuario ya existe!',
                })
        return render(request, 'sing-up.html', {
            'form': UserCreationForm,
            'error': '¡Las contraseñas no coinciden!',
        })


def logout(request):
    auth_logout(request)
    return redirect('login')


def error_404(request, exception):
    return render(request, 'error-404.html', {
        'user': request.user,
    }, status=404)


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
