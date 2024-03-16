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
                'error': 'Incorrect username or password',
            })
        else:
            auth_login(request, user)
            return redirect('academic-management')


# The next lines are only used to see how the base HTML looks like
def base_screen(request):
    return render(request, 'layouts/base-app-pages.html', {
        'user_name': "Carlos",
        'title': 'Main page',
    })


def academic_management(request):
    return render(request, 'academic-management.html', {
        'user_name': 'Esteban',
        'title': 'Academic Management',
    })


def sing_up(request):
    if request.method == 'GET':
        return render(request, 'sing-up.html', {
            'form': UserCreationForm,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                auth_login(request, user)
                return redirect('academic-management')
            except IntegrityError:
                return render(request, 'sing-up.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists!',
                })
        return render(request, 'sing-up.html', {
            'form': UserCreationForm,
            'error': 'Password does not match!',
        })


def logout(request):
    auth_logout(request)
    return redirect('login')
