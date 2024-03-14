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
#         'user_name': "Carlos",
         'title': 'Main page',
     })

def edit_screen(request):
     return render(request, 'layouts/edit-info-class.html', {
         'user_name': "David",
         'title': 'Editor de materia',
     })
#prototype
def edit(request, nrc):
     subject = subject.objects.filter(id=nrc).first()
     form = SubjectForm(instance=subject)
     return render(request, "Edit-info-class.html", {"form":form, "subject":subject})

