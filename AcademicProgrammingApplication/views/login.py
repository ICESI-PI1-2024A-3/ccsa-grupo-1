from django.shortcuts import render
from django.contrib.auth import authenticate
from AcademicProgrammingApplication.forms import UserForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect


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
