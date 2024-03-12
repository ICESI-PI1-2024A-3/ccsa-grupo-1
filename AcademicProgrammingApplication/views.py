from django.shortcuts import render
from .forms import UserForm
from .models import Subject, Class

# Create your views here.
def login(request):
    # print(request.POST)
    return render(request, 'login.html', {
        'form': UserForm()
    })

def subject_detail(request, subject_id):
    subject = Subject.objects.get(code=subject_id)
    classes = Class.objects.filter(subject=subject)  # Obtiene todas las clases relacionadas con la materia
    return render(request, 'subject_detail.html', {'subject': subject, 'classes': classes, 'title': 'Gestión de MATERIA'})


# The next lines are only used to see how the base HTML looks like
def base_screen(request):
    return render(request, 'layouts/base-app-pages.html', {
        'user_name': "Carlos",
        'title': 'Main page',
    })
