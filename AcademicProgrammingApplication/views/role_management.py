from django.shortcuts import render


def role_management(request):
    user = request.user
    return render(request, 'role-management.html', {
        'title': 'Gestión de roles',
        'user_name': user.username,
    })
