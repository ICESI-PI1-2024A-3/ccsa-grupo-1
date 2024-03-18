from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.db import IntegrityError


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
