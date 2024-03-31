from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'sign-up.html', {
            'form': UserCreationForm,
        })
    else:
        username = request.POST['username']
        if not username:
            return render(request, 'sign-up.html', {
                'form': UserCreationForm,
                'error': '¡Todos los campos son obligatorios!',
            })

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'],
                                                email=request.POST['email'],
                                                is_superuser=True if request.POST['rol'] == 'Administrador' else False)
                user.save()
                auth_login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'sign-up.html', {
                    'form': UserCreationForm,
                    'error': '¡El usuario ya existe!',
                })
        return render(request, 'sign-up.html', {
            'form': UserCreationForm,
            'error': '¡Las contraseñas no coinciden!',
        })
