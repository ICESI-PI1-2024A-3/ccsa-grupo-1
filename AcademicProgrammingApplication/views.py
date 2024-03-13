from django.shortcuts import render
from .forms import UserForm
from django.http import JsonResponse


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

def spam(request):
    return render(request, 'SpamDate.html', {
        'user_name': "Carlos",
        'title': 'Main page',
    })  

def data_processor_lounge(request):
    if request.method == 'POST':
        try:
            # Access data sent from the frontend
            datos_json = request.POST.get('datos')
            # Process the data as needed
            return JsonResponse({'mensaje': 'Datos procesados correctamente'})
        except Exception as e:
            # If any error occurs during data processing,
            # returns an error message
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
