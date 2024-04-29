from django.shortcuts import render
from AcademicProgrammingApplication.models import User, Role


def role_management(request):
    user = request.user
    current_user_id = request.user.id
    admin_role = Role.objects.get(name='Administrador')
    filtered_users = User.objects.exclude(id=current_user_id).exclude(is_superuser=True).exclude(role=admin_role)

    if request.POST:
        for i in range(0, len(filtered_users)):
            user = filtered_users[i]
            role = Role.objects.get(name=request.POST[f'role{i + 1}'])
            user.role = role
            user.save()

    return render(request, 'role-management.html', {
        'title': 'Gestión de roles',
        'user_name': user.username,
        'users': filtered_users,
    })
