from django.shortcuts import render
from .forms import UserForm


# Create your views here.
def login(request):
    # print(request.POST)
    return render(request, 'login.html', {
        'form': UserForm()
    })
