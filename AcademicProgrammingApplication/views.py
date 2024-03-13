from django.shortcuts import render
from .forms import UserForm


# Create your views here.
def login(request):
    # print(request.POST)
    return render(request, 'login.html', {
        'form': UserForm()
    })


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
