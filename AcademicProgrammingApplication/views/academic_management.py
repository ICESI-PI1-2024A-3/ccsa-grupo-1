from django.shortcuts import render


def academic_management(request):
    program = request.GET.get('program')
    academic_period = request.GET.get('academic-period')
    print(program, academic_period)
    user = request.user
    return render(request, 'academic-management.html', {
        'title': 'Programación académica',
        'user_name': user.username,
    })
