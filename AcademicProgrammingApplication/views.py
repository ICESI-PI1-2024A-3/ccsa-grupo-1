from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import Teacher, Class
from django.db.models import Q


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
    # Get the teacher searched
    teacher = teachers.first()
    # Return the 'assign-teacher.html' template with the provided context
    return render(request, 'assign-teacher.html', {
        'user_name': user.username,
        'title': 'Asignar Profesor a Clase',
        'teacher': teacher,
        'classes': get_classes(request, teacher),
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