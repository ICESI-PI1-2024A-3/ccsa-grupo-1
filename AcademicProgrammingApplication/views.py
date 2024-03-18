from django.shortcuts import render
from .forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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

@csrf_exempt
def data_processor_lounge(request):
    if request.method == 'POST':
        try:
            # Access JSON data sent from the frontend
            datos_json = json.loads(request.body)
            
            # Process the data as needed
            
            # Return a JSON response indicating success
            print(datos_json)
            print(type(datos_json))
            return JsonResponse({'mensaje': 'Datos procesados correctamente'})
        except Exception as e:
            # If any error occurs during data processing,
            # return an error message
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a JSON response indicating that the method is not allowed
        return JsonResponse({'error': 'Método no permitido'}, status=405)