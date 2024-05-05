from django.shortcuts import render
from AcademicProgrammingApplication.models import User, Role
from django.db.models import Q
from django.contrib.auth.decorators import permission_required


@permission_required('AcademicProgrammingApplication.change_role', raise_exception=True)
def role_management(request):
    user = request.user
    current_user_id = request.user.id
    admin_role = Role.objects.get(name='Administrador')
    filtered_users = User.objects.exclude(id=current_user_id).exclude(is_superuser=True).exclude(role=admin_role)
    total_users = filtered_users.count()
    queryset = request.GET.get('user_search_engine', '')
    query = False if not queryset else True
    # Filter users based on search query
    if queryset:
        filtered_users = filtered_users.filter(
            Q(username__icontains=queryset) |
            Q(first_name__icontains=queryset) |
            Q(last_name__icontains=queryset)
        ).distinct()
    show_all = total_users == filtered_users.count()
    if request.POST:
        for i in range(0, len(filtered_users)):
            user_in_list = filtered_users[i]
            user_role = Role.objects.get(name=request.POST[f'role{i + 1}'])
            user_in_list.role = user_role
            user_in_list.save()

    return render(request, 'role-management.html', {
        'title': 'Gestión de roles',
        'change_role_permission': user.has_perm('AcademicProgrammingApplication.change_role'),
        'user_name': user.username,
        'user_role': user.role,
        'users': filtered_users,
        'show_all': show_all,
        'query': query,
    })
