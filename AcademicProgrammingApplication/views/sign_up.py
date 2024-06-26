from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.shortcuts import redirect
from AcademicProgrammingApplication.models import User, Role
from django.contrib.auth.decorators import permission_required


@permission_required('AcademicProgrammingApplication.change_role', raise_exception=True)
def sign_up(request):
    """
    Handles user sign-up process.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page for user sign-up.
    """
    if request.method == 'GET':
        # Render the sign-up page with the user creation form
        return render(request, 'sign-up.html', {
            'form': UserCreationForm,
        })
    else:
        username = request.POST['username']
        if not username:
            # If username is not provided, render the sign-up page with an error message
            return render(request, 'sign-up.html', {
                'form': UserCreationForm,
                'error': '¡Todos los campos son obligatorios!',
            })

        if request.POST['password1'] == request.POST['password2']:
            try:
                role = Role.objects.get(name=request.POST['role'])
                # Create a new user with the provided information
                user = User.objects.create_user(username=request.POST['username'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'],
                                                email=request.POST['email'],
                                                password=request.POST['password1'],
                                                role=role)
                user.save()
                return redirect('role_management')
            except IntegrityError:
                # If the username already exists, render the sign-up page with an error message
                return render(request, 'sign-up.html', {
                    'form': UserCreationForm,
                    'error': '¡El usuario ya existe!',
                })
        # If passwords don't match, render the sign-up page with an error message
        return render(request, 'sign-up.html', {
            'form': UserCreationForm,
            'error': '¡Las contraseñas no coinciden!',
        })
