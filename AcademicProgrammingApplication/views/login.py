from django.shortcuts import render
from django.contrib.auth import authenticate
from AcademicProgrammingApplication.forms import UserForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect


def login(request):
    """
    Handles user authentication and login.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page for login.
    """
    if request.method == 'GET':
        # Render the login page with an empty UserForm
        return render(request, 'login.html', {
            'form': UserForm()
        })
    else:
        # Verify the username and password obtained in the login form
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # If authentication fails, render the login page with an error message
            return render(request, 'login.html', {
                'form': UserForm(),
                'error': 'Nombre de usuario o contraseña incorrectos.',
            })
        else:
            # If authentication succeeds, log in the user and redirect to the home page
            auth_login(request, user)
            return redirect('home')
