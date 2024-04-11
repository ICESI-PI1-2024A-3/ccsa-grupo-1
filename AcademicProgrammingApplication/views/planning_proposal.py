from django.shortcuts import render
from AcademicProgrammingApplication.models import Class

def planning_proposal(request):
    user = request.user

    return render(request, 'academic-programming-proposal.html', {
        'user_name': user.username,
        'title': 'Propuesta Programacion Academica',
    })

